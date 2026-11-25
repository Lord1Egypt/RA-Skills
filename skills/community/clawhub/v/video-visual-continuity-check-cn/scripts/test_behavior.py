#!/usr/bin/env python3
"""Independent examples for attribution, transitions, and textual picture evidence."""
import atexit
import shutil
import unittest
from copy import deepcopy
from pathlib import Path
from check_continuity import actor_scoped_prop, check, named_actors

# Running unittest directly can create bytecode files beside this public skill.
# Remove those local artifacts on exit so they cannot enter a future package.
atexit.register(
    lambda cache_dir=Path(__file__).parent / "__pycache__": shutil.rmtree(cache_dir, ignore_errors=True)
)

REF = {'character': {'林岚': '深蓝外套', '陈默': '白色外套'}, 'scene': '书店门口，暖光从左侧'}
FIRST = {'id': '01', 'character': '林岚穿深蓝外套', 'prop': '右手拿黄色纸袋', 'lighting': '暖光从左侧', 'space': '书店门口'}

class Behavior(unittest.TestCase):
    def categories(self, data):
        result = check(data)
        self.assertEqual(result['status'], 'ok')
        return {item['category'] for item in result['issues']}, result

    def test_different_people_not_wardrobe_or_prop_change(self):
        second = {'id': '02', 'character': '陈默穿白色外套', 'prop': '双手空着', 'lighting': '暖光从左侧', 'space': '书店门口'}
        kinds, _ = self.categories({'references': REF, 'shots': [FIRST, second]})
        self.assertEqual(kinds, set())

    def test_single_reference_does_not_apply_to_other_person(self):
        result = check({'references': {'character': '林岚：深蓝外套'}, 'shots': [
            {'id': '01', 'character': '林岚穿深蓝外套'}, {'id': '02', 'character': '陈默穿白外套'}]})
        self.assertEqual(result['status'], 'needs_material')
        self.assertIn('references.character（陈默，shots[2]涉及人物）', result['missing'])

    def test_description_only_conflicts_and_reference_dedup(self):
        kinds, result = self.categories({'references': REF, 'shots': [
            {'id': '01', 'description': '林岚穿深蓝外套，右手拿黄色纸袋，书店门口，暖光从左侧'},
            {'id': '02', 'description': '林岚穿白色外套，双手空着，咖啡店门口，暖光从右侧'}]})
        self.assertEqual(kinds, {'角色', '道具', '光线', '空间'})
        self.assertEqual(len(result['issues']), 4)
        self.assertTrue(all(item['shots'] == ['01', '02'] for item in result['issues']))

    def test_visual_only_is_actually_checked(self):
        kinds, _ = self.categories({'references': {'character': '林岚：深蓝外套'}, 'shots': [
            {'id': '01', 'visual': '林岚穿白色外套'}]})
        self.assertEqual(kinds, {'角色'})

    def test_description_explains_all_changes_including_reference(self):
        kinds, _ = self.categories({'references': REF, 'shots': [FIRST,
            {'id': '02', 'description': '林岚换上白色外套，放下纸袋后双手空着，走到咖啡店，开灯后冷光从右侧'}]})
        self.assertEqual(kinds, set())

    def test_description_and_visual_explicitly_explain_prop_position_change(self):
        for field in ('description', 'visual'):
            with self.subTest(field=field):
                kinds, _ = self.categories({'references': {'character': '林岚：深蓝外套'}, 'shots': [
                    {'id': '01', 'character': '林岚穿深蓝外套', field: '右手拿手机'},
                    {'id': '02', 'character': '林岚穿深蓝外套', field: '把手机放在桌上'},
                ]})
                self.assertNotIn('道具', kinds)

    def test_future_intentions_do_not_explain_wardrobe_or_prop_changes(self):
        current = {'id': '02', 'character': '林岚即将换上白色外套', 'prop': '准备放下纸袋，双手空着'}
        kinds, _ = self.categories({'references': REF, 'shots': [FIRST, current]})
        self.assertTrue({'角色', '道具'} <= kinds)

    def test_transition_dict_is_category_specific(self):
        second = {'id': '02', 'character': '林岚穿白色外套', 'prop': '双手空着', 'lighting': '暖光从右侧', 'space': '咖啡店门口', 'transition': {'prop': '放下纸袋'}}
        kinds, _ = self.categories({'references': REF, 'shots': [FIRST, second]})
        self.assertEqual(kinds, {'角色', '光线', '空间'})

    def test_transition_string_is_not_blanket_permission(self):
        second = {'id': '02', 'character': '林岚穿白色外套', 'prop': '双手空着', 'lighting': '暖光从右侧', 'space': '咖啡店门口', 'transition': '放下纸袋'}
        kinds, _ = self.categories({'references': REF, 'shots': [FIRST, second]})
        self.assertEqual(kinds, {'角色', '光线', '空间'})

    def test_negated_wardrobe_transition_not_an_explanation(self):
        second = {'id': '02', 'character': '林岚穿白色外套', 'transition': {'character': '没有换装'}}
        kinds, _ = self.categories({'references': {'character': '林岚：深蓝外套'}, 'shots': [FIRST | {'lighting': '', 'space': ''}, second]})
        self.assertEqual(kinds, {'角色'})

    def test_negated_prop_transition_not_an_explanation(self):
        second = {'id': '02', 'character': '林岚穿深蓝外套', 'prop': '双手空着', 'description': '没有放下纸袋'}
        kinds, _ = self.categories({'references': REF, 'shots': [FIRST, second]})
        self.assertEqual(kinds, {'道具'})

    def test_refused_or_failed_transition_is_not_an_explanation(self):
        prop, _ = self.categories({'references': REF, 'shots': [FIRST,
            {'id': '02', 'character': '林岚穿深蓝外套', 'prop': '双手空着',
             'transition': {'prop': '拒绝放下纸袋'}}]})
        self.assertIn('道具', prop)
        space, _ = self.categories({'references': {'scene': '书店'}, 'shots': [
            {'id': '01', 'space': '书店'},
            {'id': '02', 'space': '咖啡店', 'transition': {'space': '试图走进咖啡店但失败'}},
        ]})
        self.assertIn('空间', space)

    def test_facing_direction_not_light_direction(self):
        kinds, _ = self.categories({'references': REF, 'shots': [
            {'id': '01', 'description': '林岚穿深蓝外套，面向右，书店门口，暖光从左侧'}]})
        self.assertEqual(kinds, set())

    def test_generic_door_does_not_hide_building_change(self):
        kinds, result = self.categories({'references': REF, 'shots': [FIRST, {'id': '02', 'space': '咖啡店门口'}]})
        self.assertEqual(kinds, {'空间'})
        self.assertEqual(len(result['issues']), 1)

    def test_description_subject_and_scene_require_references(self):
        result = check({'references': {}, 'shots': [{'id': '01', 'description': '林岚穿深蓝外套，书店门口'}]})
        self.assertEqual(result['status'], 'needs_material')
        self.assertTrue(any('references.character' in item for item in result['missing']))
        self.assertTrue(any('references.scene' in item for item in result['missing']))

    def test_ambiguous_pronouns_not_assumed_same_person(self):
        kinds, result = self.categories({'references': {'character': '成年女性'}, 'shots': [
            {'id': '01', 'character': '她穿深蓝外套'}, {'id': '02', 'character': '她穿白色外套'}]})
        self.assertEqual(kinds, set())
        self.assertIn('notes', result)

    def test_duplicate_ids_and_missing_picture_fail(self):
        result = check({'references': {'scene': '书店'}, 'shots': [{'id': 'same', 'space': '书店'}, {'id': 'same'}]})
        self.assertEqual(result['status'], 'needs_material')
        self.assertTrue(any('重复' in item for item in result['missing']))
        self.assertTrue(any('画面信息' in item for item in result['missing']))

    def test_prop_only_does_not_require_unrelated_references(self):
        kinds, _ = self.categories({'shots': [{'id': '01', 'prop': '桌上有纸袋'}]})
        self.assertEqual(kinds, set())

    def test_generic_person_and_scene_require_references(self):
        result = check({'shots': [{'id': '01', 'description': '一位老人坐在海滩边'}]})
        self.assertEqual(result['status'], 'needs_material')
        self.assertTrue(any('references.character' in x for x in result['missing']))
        self.assertTrue(any('references.scene' in x for x in result['missing']))

    def test_named_actor_without_character_reference_is_missing_material(self):
        result = check({'references': {'scene': '卧室'}, 'shots': [
            {'id': '01', 'description': '林岚坐在卧室'}]})
        self.assertEqual(result['status'], 'needs_material')
        self.assertTrue(any('references.character' in x for x in result['missing']))

    def test_group_presence_names_require_each_character_reference(self):
        for wording in ('林岚和陈默同框', '林岚与陈默出现在书店'):
            with self.subTest(wording=wording):
                result = check({'references': {'character': {'林岚': '深蓝外套'}, 'scene': '书店'}, 'shots': [
                    {'id': '01', 'character': wording, 'space': '书店'}]})
                self.assertEqual(result['status'], 'needs_material')
                self.assertTrue(any('references.character（陈默，shots[1]涉及人物）' == item
                                    for item in result['missing']), result)

    def test_name_after_camera_prefix_requires_character_reference(self):
        result = check({'references': {'scene': '卧室'}, 'shots': [
            {'id': '01', 'description': '镜头中林岚坐在卧室'}]})
        self.assertEqual(result['status'], 'needs_material')
        self.assertTrue(any('references.character' in x for x in result['missing']))

    def test_absent_prop_does_not_invent_a_person(self):
        for description in ('桌上没有手机', '桌上没有花瓶'):
            with self.subTest(description=description):
                result = check({'shots': [{'id': '01', 'description': description}]})
                self.assertEqual(result['status'], 'ok')
                self.assertFalse(any('references.character' in x for x in result['missing']))

    def test_prop_only_shots_do_not_require_character_reference(self):
        # “停在” and “拿在” can describe an object state; neither makes the
        # prop itself a named on-screen person.
        for prop in ('相机停在桌上', '杯子拿在左手'):
            with self.subTest(prop=prop):
                result = check({'shots': [{'id': '01', 'prop': prop}]})
                self.assertEqual(result['status'], 'ok')
                self.assertFalse(any('references.character' in item for item in result['missing']), result)

    def test_empty_frame_and_still_life_do_not_require_character_reference(self):
        examples = [
            {'character': '无人出镜', 'prop': '桌上放着红色杯子'},
            {'description': '花瓶放在桌上'},
        ]
        for shot in examples:
            with self.subTest(shot=shot):
                result = check({'shots': [{'id': '01', **shot}]})
                self.assertEqual(result['status'], 'ok')
                self.assertFalse(any('references.character' in item for item in result['missing']))

    def test_explicit_unlisted_places_are_compared(self):
        result = check({'references': {'scene': '古堡大厅'}, 'shots': [
            {'id': '01', 'space': '古堡大厅内景'},
            {'id': '02', 'space': '废弃工厂大厅'},
        ]})
        self.assertEqual(result['status'], 'ok')
        self.assertTrue(any(item['category'] == '空间' and item['aspect'] == '地点'
                            for item in result['issues']), result)

    def test_generalized_place_and_color_do_not_claim_a_conflict(self):
        place = check({'references': {'scene': '卧室'}, 'shots': [
            {'id': '01', 'space': '房间空镜'},
        ]})
        color = check({'references': {'character': {'林岚': '深蓝外套'}}, 'shots': [
            {'id': '01', 'character': '林岚穿蓝色外套'},
        ]})
        self.assertFalse(place['issues'], place)
        self.assertFalse(color['issues'], color)

    def test_room_inside_alias_matches_room_reference(self):
        for place in ('卧室', '办公室'):
            with self.subTest(place=place):
                result = check({'references': {'scene': place}, 'shots': [
                    {'id': '01', 'space': f'{place}内'}]})
                self.assertEqual(result['status'], 'ok')
                self.assertFalse(result['issues'])

    def test_scene_and_prop_subjects_are_not_inferred_as_characters(self):
        for description in ('镜头推进，房门打开', '汽车进入停车场'):
            with self.subTest(description=description):
                result = check({'references': {'scene': '停车场'}, 'shots': [
                    {'id': '01', 'description': description}]})
                self.assertEqual(result['status'], 'ok')
                self.assertFalse(any('references.character' in x for x in result['missing']))

    def test_multiple_named_people_are_satisfied_by_complete_references(self):
        result = check({'references': {'character': {'林岚': '深蓝外套', '陈默': '白色外套'}, 'scene': '书店'}, 'shots': [
            {'id': '01', 'character': '林岚穿深蓝外套，陈默穿白色外套', 'space': '书店'}]})
        self.assertEqual(result['status'], 'ok')
        self.assertFalse(any('references.character' in x for x in result['missing']))

    def test_explicit_character_id_does_not_hide_other_named_people(self):
        result = check({'references': {'character': {'林岚': '黑色外套', '陈默': '白色外套'}}, 'shots': [
            {'id': '01', 'character_id': '林岚', 'character': '林岚穿白色外套，陈默穿黑色外套'}]})
        conflicts = [item for item in result['issues'] if item['category'] == '角色']
        self.assertEqual(len(conflicts), 2, result)

    def test_different_named_people_do_not_share_prop_identity(self):
        kinds, _ = self.categories({'references': {'character': {'林岚': '深蓝外套', '陈默': '白色外套'}}, 'shots': [
            {'id': '01', 'character': '林岚穿深蓝外套，林岚拿红色手机'},
            {'id': '02', 'character': '陈默穿白色外套，陈默拿蓝色手机'}]})
        self.assertNotIn('道具', kinds)

    def test_smile_requires_character_reference(self):
        result = check({'references': {'scene': '卧室'}, 'shots': [
            {'id': '01', 'description': '林岚微笑，卧室内'}]})
        self.assertEqual(result['status'], 'needs_material')
        self.assertTrue(any('references.character' in item for item in result['missing']))

    def test_unlisted_named_action_requires_character_reference(self):
        result = check({'references': {'scene': '卧室'}, 'shots': [
            {'id': '01', 'description': '林岚沉思，卧室内'}]})
        self.assertEqual(result['status'], 'needs_material')
        self.assertTrue(any('references.character' in item for item in result['missing']))

    def test_named_action_after_framing_requires_character_reference(self):
        result = check({'references': {'scene': '窗边'}, 'shots': [
            {'id': '01', 'description': '近景，林岚凝视窗外'}]})
        self.assertEqual(result['status'], 'needs_material')
        self.assertTrue(any('references.character（林岚' in item for item in result['missing']))

    def test_scene_objects_are_not_people(self):
        for scene, description in (
            ('森林', '林木摇曳，暖光从左侧'),
            ('山顶', '白云飘动，山顶远景'),
        ):
            with self.subTest(description=description):
                result = check({'references': {'scene': scene}, 'shots': [
                    {'id': '01', 'description': description}]})
                self.assertEqual(result['status'], 'ok')
                self.assertFalse(any('references.character' in item for item in result['missing']), result)

    def test_intra_shot_character_and_lighting_conflicts_are_reported(self):
        result = check({'references': {'character': {'林岚': '深蓝外套'}, 'scene': '室内暖光'}, 'shots': [
            {'id': '01', 'character': '林岚穿深蓝外套',
             'description': '林岚穿白色外套，暖光从右侧', 'lighting': '暖光从左侧'}]})
        self.assertTrue({'外套', '来光方向'} <= {item['aspect'] for item in result['issues']}, result)

    def test_one_prop_transition_does_not_explain_another_props_position(self):
        kinds, result = self.categories({'references': {'character': {'林岚': '深蓝外套'}}, 'shots': [
            {'id': '01', 'character': '林岚穿深蓝外套', 'prop': '右手拿手机，左手拿纸袋'},
            {'id': '02', 'character': '林岚穿深蓝外套', 'prop': '放下纸袋，手机在桌上'},
        ]})
        self.assertIn('道具', kinds)
        self.assertTrue(any(item['aspect'] == '手机位置' for item in result['issues']), result)

    def test_named_bedside_scene_requires_scene_reference(self):
        result = check({'shots': [{'id': '01', 'visual': '卧室床边，清晨'}]})
        self.assertEqual(result['status'], 'needs_material')
        self.assertTrue(any('references.scene' in item for item in result['missing']))

    def test_unlisted_terse_scene_requires_scene_reference(self):
        result = check({'shots': [{'id': '01', 'visual': '古堡大厅，清晨'}]})
        self.assertEqual(result['status'], 'needs_material')
        self.assertTrue(any('references.scene' in item for item in result['missing']))

    def test_common_terse_scenes_in_visual_require_scene_reference(self):
        for visual in ('书房，清晨', '教室，白天'):
            with self.subTest(visual=visual):
                result = check({'shots': [{'id': '01', 'visual': visual}]})
                self.assertEqual(result['status'], 'needs_material')
                self.assertTrue(any('references.scene' in item for item in result['missing']))

    def test_numeric_shot_id_is_valid(self):
        result = check({'shots': [{'id': 1, 'prop': '桌上有纸袋'}]})
        self.assertEqual(result['status'], 'ok')
        self.assertFalse(any('.id' in x for x in result['missing']))

    def test_named_actor_in_ordinary_state_requires_character_reference(self):
        result = check({'references': {'scene': '卧室'}, 'shots': [
            {'id': '01', 'description': '林岚在卧室静坐'}]})
        self.assertEqual(result['status'], 'needs_material')
        self.assertTrue(any('references.character' in x for x in result['missing']))

    def test_named_actor_without_scarf_is_reported_against_reference(self):
        kinds, result = self.categories({'references': {'character': '林岚：红围巾', 'scene': '卧室'}, 'shots': [
            {'id': '01', 'character': '林岚戴红围巾', 'space': '卧室'},
            {'id': '02', 'character': '林岚没有围巾', 'space': '卧室'}]})
        self.assertIn('角色', kinds)
        self.assertTrue(any(item['aspect'] == '围巾' for item in result['issues']))

    def test_name_is_not_extended_into_right_hand_possession_phrase(self):
        result = check({'references': {'character': {'林岚': '深蓝外套'}}, 'shots': [
            {'id': '01', 'character': '林岚穿深蓝外套，右手拿黄色纸袋'}]})
        self.assertEqual(result['status'], 'ok')
        self.assertEqual(result['missing'], [])

    def test_holder_phrase_does_not_turn_right_hand_into_a_second_person(self):
        result = check({'references': {'character': {'林岚': '深蓝外套'}}, 'shots': [
            {'id': '01', 'prop': '林岚右手拿黄色纸袋'}]})
        self.assertEqual(result['status'], 'ok')
        self.assertEqual(result['missing'], [])

    def test_explicit_colour_shades_and_coloured_props_are_not_collapsed(self):
        clothes = check({'references': {'character': {'林岚': '深蓝外套'}}, 'shots': [
            {'id': '01', 'character': '林岚穿深蓝外套'},
            {'id': '02', 'character': '林岚穿浅蓝外套'},
        ]})
        props = check({'references': {'character': {'林岚': '深蓝外套'}}, 'shots': [
            {'id': '01', 'character': '林岚穿深蓝外套', 'prop': '林岚拿深蓝色手机'},
            {'id': '02', 'character': '林岚穿深蓝外套', 'prop': '林岚拿红色手机'},
        ]})
        self.assertTrue(any(item['aspect'] == '外套' for item in clothes['issues']), clothes)
        self.assertTrue(any(item['aspect'] == '林岚的手机外观颜色' for item in props['issues']), props)

    def test_medium_length_hair_is_one_specific_state(self):
        result = check({'references': {'character': {'林岚': '中长发'}}, 'shots': [
            {'id': '01', 'character': '林岚中长发'},
            {'id': '02', 'character': '林岚短发'},
        ]})
        self.assertTrue(any(item['aspect'] == '头发' for item in result['issues']), result)

    def test_documented_scene_and_light_changes_carry_new_baselines(self):
        result = check({'references': {'scene': '书店，暖光从左侧'}, 'shots': [
            {'id': '01', 'space': '书店', 'lighting': '暖光从左侧'},
            {'id': '02', 'space': '进入咖啡店', 'lighting': '冷光从右侧',
             'transition': {'space': '进入咖啡店', 'lighting': '灯光转为冷光从右侧'}},
            {'id': '03', 'description': '空镜'},
            {'id': '04', 'space': '酒馆', 'lighting': '暖光从左侧'},
        ]})
        self.assertTrue(any(item['category'] == '空间' and item['shots'] == ['02', '04'] for item in result['issues']), result)
        self.assertTrue(any(item['category'] == '光线' and item['shots'] == ['02', '04'] for item in result['issues']), result)

    def test_leading_furniture_phrase_does_not_hide_known_actor(self):
        result = check({'references': {'character': {'林岚': '深蓝外套'}, 'scene': '客厅'}, 'shots': [
            {'id': '01', 'description': '沙发上坐着林岚穿深蓝外套', 'space': '客厅'},
            {'id': '02', 'description': '桌边坐着林岚穿浅蓝外套', 'space': '客厅'},
        ]})
        self.assertEqual(result['status'], 'ok')
        self.assertTrue(any(item['aspect'] == '外套' for item in result['issues']), result)

    def test_reverse_hand_word_order_is_a_hand_change(self):
        result = check({'references': {'character': {'林岚': '深蓝外套'}}, 'shots': [
            {'id': '01', 'character': '林岚穿深蓝外套', 'prop': '纸袋在右手'},
            {'id': '02', 'character': '林岚穿深蓝外套', 'prop': '纸袋在左手'},
        ]})
        self.assertTrue(any(item['aspect'] == '纸袋持有手侧' for item in result['issues']), result)

    def test_multi_person_props_are_compared_by_named_holder(self):
        first = {'id': '01', 'character': '林岚和陈默同框', 'prop': '林岚：右手持红色手机；陈默：左手持蓝色手机'}
        second = {'id': '02', 'character': '林岚和陈默同框', 'prop': '林岚：右手持红色手机；陈默：左手持蓝色手机'}
        kinds, _ = self.categories({'references': {'character': {'林岚': '深蓝外套', '陈默': '白色外套'}}, 'shots': [first, second]})
        self.assertNotIn('道具', kinds)

    def test_prop_holder_labels_align_people_when_character_field_is_generic(self):
        first = {'id': '01', 'character': '两人同框', 'prop': '林岚：右手持红色手机\n陈默：左手持蓝色手机'}
        second = {'id': '02', 'character': '两人同框', 'prop': '林岚：右手持红色手机\n陈默：左手持蓝色手机'}
        kinds, result = self.categories({'references': {'character': {'林岚': '深蓝外套', '陈默': '白色外套'}}, 'shots': [first, second]})
        self.assertNotIn('道具', kinds, result)

    def test_unattributed_held_prop_in_multi_person_scene_requests_attribution(self):
        result = check({'references': {'character': {'林岚': '深蓝外套', '陈默': '白色外套'}}, 'shots': [
            {'id': '01', 'character': '林岚和陈默同框', 'prop': '右手拿纸袋'},
            {'id': '02', 'character': '林岚和陈默同框', 'prop': '双手空着'}]})
        self.assertEqual(result['status'], 'needs_material')
        self.assertTrue(any('标注道具持有人' in item for item in result['missing']))

    def test_unattributed_prop_clause_after_named_person_still_needs_holder(self):
        result = check({'references': {'character': {'林岚': '深蓝外套', '陈默': '白色外套'}}, 'shots': [
            {'id': '01', 'character': '林岚和陈默同框', 'prop': '林岚拿手机；右手拿纸袋'}]})
        self.assertEqual(result['status'], 'needs_material')
        self.assertTrue(any('唯一持有人' in item for item in result['missing']))

    def test_unattributed_clause_is_not_inherited_by_previous_actor(self):
        references = {'character': {'林岚': '深蓝外套', '陈默': '白色外套'}}
        shot = {'id': '01', 'character': '林岚和陈默同框', 'prop': '林岚拿手机；右手拿纸袋'}
        self.assertNotIn('纸袋', actor_scoped_prop(shot, '林岚', references))

    def test_place_parser_stops_before_person_activity(self):
        for wording in ('林岚在卧室静坐', '林岚在书店看书', '林岚在办公室等待'):
            with self.subTest(wording=wording):
                kinds, result = self.categories({'references': {'character': {'林岚': '深蓝外套'}, 'scene': wording.split('在')[1].split('静坐')[0].split('看书')[0].split('等待')[0]}, 'shots': [
                    {'id': '01', 'character': '林岚穿深蓝外套', 'space': wording}]})
                self.assertNotIn('空间', kinds, result)

    def test_explanation_for_one_person_does_not_waive_another_person_change(self):
        kinds, _ = self.categories({'references': {'character': {'林岚': '深蓝外套', '陈默': '白色外套'}}, 'shots': [
            {'id': '01', 'character': '林岚穿深蓝外套；陈默穿白色外套'},
            {'id': '02', 'character': '林岚穿黑色外套；陈默穿白色外套', 'transition': {'character': '陈默把外套换成红色'}}]})
        self.assertIn('角色', kinds)

    def test_character_id_scopes_wardrobe_without_repeating_the_name(self):
        result = check({'references': {'character': {'林岚': '深蓝外套', '陈默': '白色外套'}}, 'shots': [
            {'id': '01', 'character_id': '林岚', 'character': '穿黑色外套'}]})
        self.assertTrue(any(item['category'] == '角色' and item['aspect'] == '外套' for item in result['issues']), result)

    def test_one_person_phone_handoff_does_not_explain_other_person_hand_change(self):
        result = check({'references': {'character': {'林岚': '深蓝外套', '陈默': '白色外套'}}, 'shots': [
            {'id': '01', 'character': '林岚和陈默同框', 'prop': '林岚右手拿手机；陈默左手拿手机'},
            {'id': '02', 'character': '林岚和陈默同框', 'prop': '林岚左手拿手机；陈默右手拿手机', 'transition': {'prop': '林岚换手拿手机'}}]})
        hand_issues = [item for item in result['issues'] if item['category'] == '道具' and item['aspect'].endswith('持有手侧')]
        self.assertTrue(any('陈默' in item['aspect'] for item in hand_issues), result)

    def test_one_person_phone_replacement_does_not_explain_other_person_color_change(self):
        result = check({'references': {'character': {'林岚': '深蓝外套', '陈默': '白色外套'}}, 'shots': [
            {'id': '01', 'character': '林岚和陈默同框', 'prop': '林岚拿红色手机；陈默拿红色手机'},
            {'id': '02', 'character': '林岚和陈默同框', 'prop': '林岚拿蓝色手机；陈默拿蓝色手机', 'transition': {'prop': '林岚更换手机'}}]})
        color_issues = [item for item in result['issues'] if item['category'] == '道具' and item['aspect'].endswith('外观颜色')]
        self.assertTrue(any('陈默' in item['aspect'] for item in color_issues), result)

    def test_inline_explanation_for_one_person_does_not_waive_another_person_change(self):
        kinds, _ = self.categories({'references': {'character': {'林岚': '深蓝外套', '陈默': '白色外套'}}, 'shots': [
            {'id': '01', 'character': '林岚穿深蓝外套；陈默穿白色外套'},
            {'id': '02', 'character': '林岚穿黑色外套；陈默把外套换成红色'}]})
        self.assertIn('角色', kinds)

    def test_one_person_prop_action_does_not_explain_another_persons_missing_prop(self):
        result = check({'references': {'character': {'林岚': '深蓝外套', '陈默': '白色外套'}}, 'shots': [
            {'id': '01', 'character': '林岚和陈默同框', 'prop': '林岚右手拿纸袋；陈默左手拿手机'},
            {'id': '02', 'character': '林岚和陈默同框', 'prop': '林岚双手空着；陈默放下纸袋'}]})
        self.assertTrue(any(item['category'] == '道具' and item['aspect'] == '纸袋' for item in result['issues']), result)

    def test_other_objects_do_not_trigger_character_material_requirement(self):
        result = check({'shots': [{'id': '01', 'description': '画面展示其他物体，其他道具放在桌上'}]})
        self.assertEqual(result['status'], 'ok')
        self.assertEqual(result['missing'], [])

    def test_explicit_jacket_change_and_scarf_removal_are_explained(self):
        jacket = check({'references': {'character': '林岚：深蓝外套'}, 'shots': [
            {'id': '01', 'character': '林岚穿深蓝外套'},
            {'id': '02', 'character': '林岚穿白色外套', 'transition': {'character': '把外套换成白色'}}]})
        self.assertFalse(any(item['category'] == '角色' for item in jacket['issues']))
        scarf = check({'references': {'character': '林岚：红围巾'}, 'shots': [
            {'id': '01', 'character': '林岚戴红围巾'},
            {'id': '02', 'character': '林岚未戴围巾', 'transition': {'character': '摘下围巾'}}]})
        self.assertFalse(any(item['category'] == '角色' for item in scarf['issues']))

    def test_walk_into_cafe_explains_space_change(self):
        result = check({'references': {'scene': '卧室'}, 'shots': [
            {'id': '01', 'space': '卧室'}, {'id': '02', 'space': '走进咖啡店'}]})
        self.assertFalse(any(item['category'] == '空间' and item['aspect'] == '地点' for item in result['issues']))

    def test_documented_change_becomes_the_next_shot_baseline(self):
        result = check({'references': {'character': '林岚：深蓝外套', 'scene': '卧室，暖光从左侧'}, 'shots': [
            {'id': '01', 'character': '林岚穿深蓝外套', 'space': '卧室', 'lighting': '暖光从左侧'},
            {'id': '02', 'character': '林岚把深蓝外套换成白色', 'space': '走进咖啡店', 'lighting': '开灯改为冷光从右侧'},
            {'id': '03', 'character': '林岚穿白色外套', 'space': '咖啡店', 'lighting': '冷光从右侧'},
        ]})
        self.assertFalse(result['issues'], result)

    def test_multi_person_coloured_or_hand_side_prop_requires_holder(self):
        references = {'character': {'林岚': '深蓝外套', '陈默': '白色外套'}}
        for prop in ('红色手机和蓝色手机', '手机在右手'):
            with self.subTest(prop=prop):
                result = check({'references': references, 'shots': [
                    {'id': '01', 'character': '林岚和陈默同框', 'prop': prop},
                    {'id': '02', 'character': '林岚和陈默同框', 'prop': prop},
                ]})
                self.assertEqual(result['status'], 'needs_material')
                self.assertTrue(any('持有人' in item for item in result['missing']), result)

    def test_named_actor_in_description_is_compared_without_wardrobe_verbs(self):
        kinds, result = self.categories({'references': {'character': '林岚：红围巾', 'scene': '卧室'}, 'shots': [
            {'id': '01', 'description': '林岚在卧室静坐，戴红围巾'},
            {'id': '02', 'description': '林岚在卧室回头，没有围巾'}]})
        self.assertIn('角色', kinds)
        self.assertTrue(any(item['aspect'] == '围巾' for item in result['issues']))

    def test_unrelated_wardrobe_action_does_not_excuse_conflict(self):
        kinds, _ = self.categories({'references': {'character': '林岚：深蓝外套'}, 'shots': [
            {'id': '01', 'character': '林岚穿深蓝外套'},
            {'id': '02', 'character': '林岚换上绿围巾，穿白色外套'}]})
        self.assertIn('角色', kinds)

    def test_unrelated_prop_action_does_not_excuse_missing_item(self):
        kinds, _ = self.categories({'references': REF, 'shots': [FIRST,
            {'id': '02', 'character': '林岚穿深蓝外套', 'prop': '拿起手机，双手空着'}]})
        self.assertIn('道具', kinds)

    def test_negated_long_form_action_does_not_explain_prop_gap(self):
        kinds, _ = self.categories({'references': REF, 'shots': [FIRST,
            {'id': '02', 'character': '林岚穿深蓝外套', 'prop': '没有把纸袋放下，但双手空着'}]})
        self.assertIn('道具', kinds)

    def test_facing_change_is_reported(self):
        kinds, _ = self.categories({'references': REF, 'shots': [
            {'id': '01', 'character': '林岚穿深蓝外套', 'space': '书店门口面向右'},
            {'id': '02', 'character': '林岚穿深蓝外套', 'space': '书店门口面向左'}]})
        self.assertIn('空间', kinds)

    def test_unlisted_places_are_compared(self):
        kinds, _ = self.categories({'references': {'character': '林岚：深蓝外套', 'scene': '海滩'}, 'shots': [
            {'id': '01', 'character': '林岚穿深蓝外套', 'space': '海滩'},
            {'id': '02', 'character': '林岚穿深蓝外套', 'space': '码头'}]})
        self.assertIn('空间', kinds)

    def test_structured_character_name_matches_reference_key(self):
        result = check({'references': {'character': {'林岚': '深蓝外套'}}, 'shots': [
            {'id': '01', 'character': '林岚', 'description': '白色外套'}]})
        self.assertTrue(any(item['aspect'] == '外套' for item in result['issues']))

    def test_specific_wardrobe_change_only_explains_that_garment(self):
        kinds, result = self.categories({'references': {'character': '林岚：深蓝外套、红围巾'}, 'shots': [
            {'id': '01', 'character': '林岚穿深蓝外套和红围巾'},
            {'id': '02', 'character': '林岚换上绿围巾，穿白色外套'}]})
        self.assertTrue(any(item['aspect'] == '外套' for item in result['issues']))
        self.assertFalse(any(item['aspect'] == '围巾' for item in result['issues']))

    def test_same_compound_place_is_not_a_false_conflict(self):
        kinds, _ = self.categories({'references': {'character': '林岚：深蓝外套', 'scene': '书店门口'}, 'shots': [
            {'id': '01', 'character': '林岚穿深蓝外套', 'space': '林岚在书店门口面向右'}]})
        self.assertNotIn('空间', kinds)

    def test_compound_places_detect_an_unexplained_scene_change(self):
        kinds, result = self.categories({'references': {'character': '林岚：深蓝外套', 'scene': '书店门口'}, 'shots': [
            {'id': '01', 'character': '林岚穿深蓝外套', 'space': '林岚在书店门口'},
            {'id': '02', 'character': '林岚穿深蓝外套', 'space': '林岚在咖啡店门口'}]})
        place_issues = [item for item in result['issues'] if item['aspect'] == '地点']
        self.assertEqual(kinds, {'空间'})
        self.assertEqual(len(place_issues), 1)
        self.assertEqual(place_issues[0]['shots'], ['01', '02'])

    def test_turn_does_not_explain_a_location_change(self):
        kinds, _ = self.categories({'references': REF, 'shots': [FIRST,
            {'id': '02', 'character': '林岚穿深蓝外套', 'space': '转身，在咖啡店门口', 'transition': '转身'}]})
        self.assertIn('空间', kinds)

    def test_turn_explains_explicit_movement_direction_change(self):
        kinds, _ = self.categories({'references': {'scene': '书店内向右走'}, 'shots': [
            {'id': '01', 'space': '书店内向右走'},
            {'id': '02', 'space': '书店内转身后向左走', 'transition': {'space': '转身'}}]})
        self.assertNotIn('空间', kinds)

    def test_negative_or_future_movement_does_not_explain_scene_change(self):
        for transition in ('没有走进咖啡店', '即将走进咖啡店'):
            kinds, _ = self.categories({'references': {'scene': '书店'}, 'shots': [
                {'id': '01', 'space': '书店'},
                {'id': '02', 'space': '咖啡店', 'transition': {'space': transition}}]})
            self.assertIn('空间', kinds, transition)

    def test_numeric_shot_id_is_safe_in_identity_note(self):
        result = check({'references': {'character': '成年女性'}, 'shots': [
            {'id': 1, 'character': '她穿白色外套'}]})
        self.assertEqual(result['status'], 'ok')
        self.assertTrue(any('镜头：1' in note for note in result.get('notes', [])), result)

    def test_bare_scene_phrases_are_not_misread_as_people(self):
        for place in ('古堡大厅', '林间小路'):
            result = check({'references': {'scene': place}, 'shots': [{'id': '01', 'space': place}]})
            self.assertEqual(result['status'], 'ok', place)
            self.assertEqual(result['missing'], [], place)
            self.assertFalse(any('地点人工核对' in item['aspect'] for item in result['issues']), place)

    def test_common_scene_description_leads_are_not_misread_as_people(self):
        for description in ('白墙反光', '朱门半开', '林间雾气弥漫', '高楼灯火通明'):
            with self.subTest(description=description):
                result = check({'references': {'scene': '室内'}, 'shots': [{'id': '01', 'description': description}]})
                self.assertEqual(result['status'], 'ok', result)
                self.assertFalse(any('references.character' in item for item in result['missing']), result)

    def test_empty_frame_and_static_vase_do_not_require_character_reference(self):
        for shot in (
            {'id': '01', 'character': '无人出镜', 'prop': '桌上放着红色杯子'},
            {'id': '01', 'description': '花瓶放在桌上'}
        ):
            result = check({'shots': [shot]})
            self.assertFalse(any('references.character' in item for item in result['missing']), result)

    def test_generic_room_and_color_words_are_not_false_conflicts(self):
        room = check({'references': {'scene': '卧室'}, 'shots': [{'id': '01', 'space': '房间空镜'}]})
        self.assertFalse(any(item['aspect'] == '地点' for item in room['issues']), room)
        color = check({'references': {'character': {'林岚': '深蓝外套'}}, 'shots': [{'id': '01', 'character': '林岚穿蓝色外套'}]})
        self.assertFalse(any(item['category'] == '角色' and item['aspect'] == '外套' for item in color['issues']), color)

    def test_unlisted_but_explicit_venue_change_is_reported(self):
        result = check({'references': {'scene': '古堡大厅'}, 'shots': [
            {'id': '01', 'space': '古堡大厅'},
            {'id': '02', 'space': '废弃工厂大厅'}]})
        self.assertTrue(any(item['category'] == '空间' and item['aspect'] == '地点' for item in result['issues']), result)

    def test_hair_and_glasses_changes_are_reported(self):
        result = check({'references': {'character': {'林岚': '长发，戴黑框眼镜'}}, 'shots': [
            {'id': '01', 'character': '林岚长发，戴黑框眼镜'},
            {'id': '02', 'character': '林岚短发，未戴眼镜'}]})
        features = {item['aspect'] for item in result['issues'] if item['category'] == '角色'}
        self.assertEqual(features, {'头发', '眼镜'}, result)

    def test_negated_character_state_is_not_a_name_and_explicit_removal_explains_it(self):
        self.assertEqual(named_actors('林岚未戴围巾'), ['林岚'])
        self.assertEqual(named_actors('林岚不戴眼镜'), ['林岚'])
        unexplained = check({'references': {'character': {'林岚': '戴黑框眼镜'}}, 'shots': [
            {'id': '01', 'character': '林岚戴黑框眼镜'},
            {'id': '02', 'character': '林岚未戴眼镜'}]})
        self.assertEqual(unexplained['status'], 'ok', unexplained)
        self.assertTrue(any(item['aspect'] == '眼镜' for item in unexplained['issues']), unexplained)
        explained = check({'references': {'character': {'林岚': '戴黑框眼镜'}}, 'shots': [
            {'id': '01', 'character': '林岚戴黑框眼镜'},
            {'id': '02', 'character': '林岚摘下眼镜，未戴眼镜', 'transition': {'character': '摘下眼镜'}}]})
        self.assertFalse(any(item['aspect'] == '眼镜' for item in explained['issues']), explained)

    def test_removed_accessory_remains_the_baseline_for_later_shots(self):
        result = check({'references': {'character': {'林岚': '红围巾'}}, 'shots': [
            {'id': '01', 'character': '林岚戴红围巾'},
            {'id': '02', 'character': '林岚摘下红围巾，未戴围巾', 'transition': {'character': '摘下红围巾'}},
            {'id': '03', 'character': '林岚戴红围巾'}]})
        self.assertTrue(any(item['aspect'] == '围巾' and item['shots'] == ['02', '03'] for item in result['issues']), result)

    def test_switching_light_on_or_off_explains_brightness_change(self):
        for before, after, action in [('昏暗暖光', '开灯后明亮暖光', '开灯'), ('明亮暖光', '关灯后昏暗暖光', '关灯')]:
            with self.subTest(action=action):
                result = check({'references': {'scene': f'卧室，{before}'}, 'shots': [
                    {'id': '01', 'space': '卧室', 'lighting': before},
                    {'id': '02', 'space': '卧室', 'lighting': after, 'transition': {'lighting': action}}]})
                self.assertFalse(any(item['aspect'] == '光线明暗' for item in result['issues']), result)

    def test_different_people_phone_positions_are_not_compared(self):
        result = check({'references': {'character': {'林岚': '深蓝外套', '陈默': '白色外套'}}, 'shots': [
            {'id': '01', 'character': '林岚穿深蓝外套', 'prop': '林岚手持手机'},
            {'id': '02', 'character': '陈默穿白色外套', 'prop': '陈默的手机在桌上'}]})
        self.assertFalse(any(item['aspect'] == '手机位置' for item in result['issues']), result)

    def test_reversed_hand_phrase_still_detects_disappearance(self):
        result = check({'references': {'character': {'林岚': '深蓝外套'}}, 'shots': [
            {'id': '01', 'character': '林岚穿深蓝外套', 'prop': '纸袋在右手'},
            {'id': '02', 'character': '林岚穿深蓝外套', 'prop': '双手空着'}]})
        self.assertTrue(any(item['category'] == '道具' and '纸袋' in item['aspect'] for item in result['issues']), result)

    def test_glasses_color_and_camera_holding_state_are_reported(self):
        glasses = check({'references': {'character': {'林岚': '戴黑色眼镜'}}, 'shots': [
            {'id': '01', 'character': '林岚戴黑色眼镜'}, {'id': '02', 'character': '林岚戴金色眼镜'}]})
        self.assertTrue(any(item['aspect'] == '眼镜' for item in glasses['issues']), glasses)
        camera = check({'references': {'character': {'林岚': '深蓝外套'}}, 'shots': [
            {'id': '01', 'character': '林岚穿深蓝外套', 'prop': '手持相机'},
            {'id': '02', 'character': '林岚穿深蓝外套', 'prop': '双手空着'}]})
        self.assertTrue(any(item['category'] == '道具' for item in camera['issues']), camera)

    def test_shades_and_intermediate_hair_lengths_remain_distinct(self):
        coat = check({'references': {'character': {'林岚': '深蓝外套'}}, 'shots': [
            {'id': '01', 'character': '林岚穿浅蓝外套'}]})
        self.assertTrue(any(item['aspect'] == '外套' for item in coat['issues']), coat)
        phone = check({'shots': [
            {'id': '01', 'prop': '深蓝色手机放在桌上'},
            {'id': '02', 'prop': '红色手机放在桌上'}]})
        self.assertTrue(any(item['aspect'] == '手机外观颜色' for item in phone['issues']), phone)
        hair = check({'references': {'character': {'林岚': '中长发'}}, 'shots': [
            {'id': '01', 'character': '林岚短发'}]})
        self.assertTrue(any(item['aspect'] == '头发' for item in hair['issues']), hair)

    def test_scene_and_light_baselines_carry_across_omitted_shots(self):
        scene = check({'references': {'scene': '书店'}, 'shots': [
            {'id': '01', 'space': '书店'},
            {'id': '02', 'space': '咖啡店', 'transition': {'space': '进入咖啡店'}},
            {'id': '03', 'description': '静物特写'},
            {'id': '04', 'space': '酒馆'}]})
        self.assertTrue(any(item['category'] == '空间' and item['shots'][-1] == '04' for item in scene['issues']), scene)
        light = check({'references': {'scene': '暖光从左侧'}, 'shots': [
            {'id': '01', 'lighting': '暖光从左侧'},
            {'id': '02', 'lighting': '冷光从右侧', 'transition': {'lighting': '重新布光为冷光从右侧'}},
            {'id': '03', 'description': '静物特写'},
            {'id': '04', 'lighting': '暖光从左侧'}]})
        self.assertTrue(any(item['category'] == '光线' and item['shots'][-1] == '04' for item in light['issues']), light)

    def test_fronted_scene_phrase_and_reversed_hand_order_are_recognized(self):
        fronted = check({'references': {'character': {'林岚': '深蓝外套'}, 'scene': '卧室'}, 'shots': [
            {'id': '01', 'description': '沙发上坐着林岚穿深蓝外套'}]})
        self.assertEqual(fronted['status'], 'ok', fronted)
        self.assertFalse(any('references.character' in item for item in fronted['missing']), fronted)
        hands = check({'references': {'character': {'林岚': '深蓝外套'}}, 'shots': [
            {'id': '01', 'character': '林岚穿深蓝外套', 'prop': '黄色纸袋在右手'},
            {'id': '02', 'character': '林岚穿深蓝外套', 'prop': '黄色纸袋在左手'}]})
        self.assertTrue(any(item['aspect'] == '纸袋持有手侧' for item in hands['issues']), hands)

    def test_prop_location_light_intensity_and_scene_anchor_changes_are_reported(self):
        prop = check({'shots': [{'id': '01', 'prop': '右手拿黄色纸袋'}, {'id': '02', 'prop': '黄色纸袋在桌上'}]})
        self.assertTrue(any(item['aspect'] == '纸袋位置' for item in prop['issues']), prop)
        light = check({'references': {'scene': '明亮暖光'}, 'shots': [{'id': '01', 'lighting': '昏暗暖光'}]})
        self.assertTrue(any(item['aspect'] == '光线明暗' for item in light['issues']), light)
        space = check({'references': {'scene': '办公桌左侧'}, 'shots': [{'id': '01', 'space': '办公桌右侧'}]})
        self.assertTrue(any(item['aspect'] == '办公桌位置' for item in space['issues']), space)

    def test_explicit_cross_category_changes_are_not_silently_accepted(self):
        result = check({'references': {
            'character': {'林岚': '长发，戴黑框眼镜'},
            'scene': '办公室，明亮暖光，办公桌左侧',
        }, 'shots': [
            {'id': '01', 'description': '林岚长发、戴黑框眼镜，右手拿黄色纸袋，明亮暖光，办公桌左侧'},
            {'id': '02', 'description': '林岚短发、未戴眼镜，黄色纸袋在桌上，昏暗暖光，办公桌右侧'},
        ]})
        self.assertEqual(result['status'], 'ok')
        aspects = {item['aspect'] for item in result['issues']}
        self.assertTrue({'头发', '眼镜', '纸袋位置', '光线明暗', '办公桌位置'} <= aspects, result)

    def test_reference_change_baseline_catches_contradiction_after_omitted_shot(self):
        result = check({'references': {'character': {'林岚': '深蓝外套'}}, 'shots': [
            {'id': '01', 'character': '林岚穿白色外套', 'transition': {'character': '林岚换上白色外套'}},
            {'id': '02', 'character': '林岚低头'},
            {'id': '03', 'character': '林岚穿红色外套'}]})
        self.assertTrue(any(item['category'] == '角色' and item['shots'] == ['01', '03'] for item in result['issues']), result)

    def test_same_unknown_studio_location_with_light_reference_is_not_a_conflict(self):
        result = check({'references': {'scene': '摄影棚，暖光从左侧'}, 'shots': [
            {'id': '01', 'space': '摄影棚'}]})
        self.assertFalse(any(item['category'] == '空间' for item in result['issues']), result)

    def test_unknown_place_details_do_not_create_a_manual_location_conflict(self):
        result = check({'references': {'scene': '摄影棚，暖光从左侧'}, 'shots': [
            {'id': '01', 'space': '摄影棚，清晨'}]})
        self.assertFalse(any(item['category'] == '空间' for item in result['issues']), result)

    def test_unknown_place_details_between_shots_do_not_create_a_manual_conflict(self):
        kinds, _ = self.categories({'references': {'scene': '摄影棚'}, 'shots': [
            {'id': '01', 'space': '摄影棚，清晨'},
            {'id': '02', 'space': '摄影棚，暖光从左侧'}]})
        self.assertNotIn('空间', kinds)

    def test_turn_explains_facing_change(self):
        kinds, result = self.categories({'references': {'character': '林岚：深蓝外套', 'scene': '书店门口面向右'}, 'shots': [
            {'id': '01', 'character': '林岚穿深蓝外套', 'space': '书店门口面向右'},
            {'id': '02', 'character': '林岚穿深蓝外套', 'space': '书店门口面向左', 'transition': {'space': '转身'}}]})
        self.assertNotIn('空间', kinds)

    def test_turn_in_current_space_description_explains_facing_change(self):
        kinds, _ = self.categories({'references': {'character': '林岚：深蓝外套', 'scene': '书店门口面向右'}, 'shots': [
            {'id': '01', 'character': '林岚穿深蓝外套', 'space': '书店门口面向右'},
            {'id': '02', 'character': '林岚穿深蓝外套', 'space': '书店门口，转身后面向左'}]})
        self.assertNotIn('空间', kinds)

    def test_prop_description_can_explain_open_closed_action(self):
        kinds, _ = self.categories({'shots': [
            {'id': '01', 'prop': '桌上的盒子打开'},
            {'id': '02', 'prop': '合上盒子，盒子关闭'}]})
        self.assertNotIn('道具', kinds)

    def test_natural_object_then_action_order_explains_open_closed_change(self):
        kinds, _ = self.categories({'shots': [
            {'id': '01', 'prop': '桌上的盒子打开'},
            {'id': '02', 'prop': '把盒子关上，盒子关闭'}]})
        self.assertNotIn('道具', kinds)

    def test_prop_action_in_description_or_visual_explains_open_closed_change(self):
        for field in ('description', 'visual'):
            with self.subTest(field=field):
                kinds, _ = self.categories({'shots': [
                    {'id': '01', 'prop': '桌上的盒子打开'},
                    {'id': '02', field: '合上盒子，盒子关闭'}]})
                self.assertNotIn('道具', kinds)

    def test_ambiguous_actor_prop_handoff_is_flagged_for_manual_review(self):
        result = check({'references': {'character': '成年女性'}, 'shots': [
            {'id': '01', 'character': '她', 'prop': '手拿纸袋'},
            {'id': '02', 'character': '她', 'prop': '双手空着'}]})
        self.assertEqual(result['status'], 'ok')
        self.assertTrue(any('身份不能安全对齐的道具变化' in note for note in result.get('notes', [])))

    def test_unlisted_explicit_locations_are_reported(self):
        kinds, result = self.categories({'references': {'scene': '天台'}, 'shots': [
            {'id': '01', 'space': '天台'}, {'id': '02', 'space': '地下室'}]})
        self.assertIn('空间', kinds)
        self.assertTrue(any(item['aspect'] == '地点' for item in result['issues']))

    def test_character_reference_must_match_explicit_id(self):
        result = check({'references': {'character': {'甲': '红围巾'}}, 'shots': [
            {'id': '01', 'character_id': '乙', 'character': '乙戴红围巾'}]})
        self.assertEqual(result['status'], 'needs_material')
        self.assertTrue(any('references.character（shots[1]' in item for item in result['missing']))

    def test_explicit_garment_disappearance_is_reported(self):
        kinds, _ = self.categories({'references': {'character': {'林岚': '红围巾'}}, 'shots': [
            {'id': '01', 'character_id': '林岚', 'character': '林岚戴红围巾'},
            {'id': '02', 'character_id': '林岚', 'character': '林岚没有围巾'}]})
        self.assertIn('角色', kinds)

    def test_prop_open_closed_state_change_is_reported(self):
        kinds, result = self.categories({'shots': [
            {'id': '01', 'prop': '桌上的盒子打开'}, {'id': '02', 'prop': '桌上的盒子关闭'}]})
        self.assertIn('道具', kinds)
        self.assertTrue(any(item['aspect'] == '盒子开合状态' for item in result['issues']))

    def test_curtain_is_not_mistaken_for_a_person(self):
        result = check({'shots': [{'id': '01', 'description': '窗帘打开'}]})
        self.assertEqual(result['status'], 'ok')
        self.assertEqual(result['missing'], [])

    def test_facing_is_not_movement(self):
        kinds, result = self.categories({'references': {'character': '林岚：深蓝外套', 'scene': '办公室'}, 'shots': [
            {'id': '01', 'character': '林岚穿深蓝外套', 'space': '面向右'}]})
        self.assertNotIn('运动方向', {item['aspect'] for item in result['issues']})

    def test_multi_person_references_check_each_person(self):
        result = check({'references': {'character': {'林岚': '深蓝外套', '陈默': '白色外套'}}, 'shots': [
            {'id': '01', 'character': '林岚穿白色外套，陈默穿黑色外套'}]})
        self.assertEqual(result['status'], 'ok')
        people = [item['evidence'] for item in result['issues'] if item['category'] == '角色']
        self.assertEqual(len(people), 2)
        self.assertTrue(any('深蓝外套' in evidence and '白外套' in evidence for evidence in people))
        self.assertTrue(any('白外套' in evidence and '黑外套' in evidence for evidence in people))

    def test_missing_reference_for_one_named_person_is_requested(self):
        result = check({'references': {'character': {'林岚': '深蓝外套'}}, 'shots': [
            {'id': '01', 'character': '林岚穿深蓝外套，陈默穿白色外套'}]})
        self.assertEqual(result['status'], 'needs_material')
        self.assertIn('references.character（陈默，shots[1]涉及人物）', result['missing'])

    def test_coordinated_people_still_require_each_reference(self):
        result = check({'references': {'character': {'陈默': '白色外套'}}, 'shots': [
            {'id': '01', 'character': '林岚、陈默同时穿白色外套'}]})
        self.assertEqual(result['status'], 'needs_material')
        self.assertIn('references.character（林岚，shots[1]涉及人物）', result['missing'])

    def test_coordinated_people_are_each_checked_against_references(self):
        result = check({'references': {'character': {'林岚': '深蓝外套', '陈默': '白色外套'}}, 'shots': [
            {'id': '01', 'character': '林岚、陈默同时穿黑色外套'}]})
        self.assertEqual(result['status'], 'ok')
        self.assertEqual(len([x for x in result['issues'] if x['category'] == '角色']), 2)

    def test_prop_color_change_is_detected(self):
        kinds, result = self.categories({'shots': [
            {'id': '01', 'prop': '桌上有红色杯子'}, {'id': '02', 'prop': '桌上有蓝色杯子'}]})
        self.assertIn('道具', kinds)
        self.assertTrue(any(item['aspect'] == '杯子外观颜色' for item in result['issues']))

    def test_light_temperature_change_is_detected(self):
        kinds, result = self.categories({'references': {'scene': '暖光'}, 'shots': [
            {'id': '01', 'lighting': '暖光'}, {'id': '02', 'lighting': '冷光'}]})
        self.assertIn('光线', kinds)
        self.assertTrue(any(item['aspect'] == '光线色温' for item in result['issues']))

    def test_frame_position_is_not_a_scene_location(self):
        kinds, result = self.categories({'references': {'scene': '办公室'}, 'shots': [
            {'id': '01', 'space': '位于画面左侧'}]})
        self.assertNotIn('空间', kinds)
        self.assertEqual(result['issues'], [])

    def test_scene_nouns_are_not_mistaken_for_people(self):
        result = check({'references': {'scene': '海平面暖光从左侧，床头有台灯'}, 'shots': [
            {'id': '01', 'description': '暖光在画面左侧，太阳出现在海平面，台灯在床头'}]})
        self.assertEqual(result['status'], 'ok')
        self.assertFalse(any('references.character' in item for item in result['missing']))

    def test_yellow_paper_bag_is_not_mistaken_for_a_person(self):
        result = check({'shots': [{'id': '01', 'description': '黄色纸袋拿在右手中'}]})
        self.assertEqual(result['status'], 'ok')
        self.assertEqual(result['missing'], [])

    def test_three_character_name_is_not_truncated(self):
        self.assertEqual(named_actors('张晓明穿黑色外套'), ['张晓明'])
        result = check({'references': {'character': {'张晓明': '白色外套'}}, 'shots': [
            {'id': '01', 'description': '张晓明穿黑色外套'}]})
        self.assertEqual(result['status'], 'ok')
        self.assertFalse(any('张晓）' in item for item in result['missing']))

    def test_unlisted_action_keeps_three_and_compound_surname_names(self):
        for name in ('李小明', '欧阳娜娜'):
            with self.subTest(name=name):
                self.assertEqual(named_actors(name + '沉思'), [name])
                result = check({'references': {'character': {name: '白色外套'}}, 'shots': [
                    {'id': '01', 'description': name + '沉思'}]})
                self.assertEqual(result['status'], 'ok')
                self.assertEqual(result['missing'], [])

    def test_ordinary_prop_is_not_a_character_without_a_reference(self):
        result = check({'shots': [{'id': '01', 'description': '黄色纸袋放在桌上'}]})
        self.assertEqual(result['status'], 'ok')
        self.assertEqual(result['missing'], [])

    def test_object_action_phrases_do_not_require_character_references(self):
        for field, wording in (
            ('prop', '相机停在桌上'),
            ('prop', '杯子拿在左手'),
            ('description', '相机停在桌上'),
            ('description', '杯子拿在左手'),
        ):
            with self.subTest(field=field, wording=wording):
                result = check({'shots': [{'id': '01', field: wording}]})
                self.assertEqual(result['status'], 'ok')
                self.assertFalse(any('references.character' in item for item in result['missing']))

    def test_named_person_with_generic_prop_action_is_still_detected(self):
        self.assertEqual(named_actors('张晓明拿着相机'), ['张晓明'])

    def test_anonymous_pronoun_does_not_join_props_across_shots(self):
        result = check({'references': {'character': '成年女性'}, 'shots': [
            {'id': '01', 'description': '她拿红色纸袋'},
            {'id': '02', 'description': '她拿蓝色纸袋'}]})
        self.assertEqual(result['status'], 'ok')
        self.assertFalse(any(item['category'] == '道具' for item in result['issues']), result)

    def test_anonymous_pronouns_do_not_align_phone_colours(self):
        result = check({'references': {'character': '成年女性'}, 'shots': [
            {'id': '01', 'character': '她', 'prop': '红色手机'},
            {'id': '02', 'character': '她', 'prop': '蓝色手机'}]})
        self.assertEqual(result['status'], 'ok')
        self.assertFalse(any(item['category'] == '道具' for item in result['issues']), result)

    def test_lighting_in_description_and_visual_requires_scene_reference(self):
        for field in ('description', 'visual'):
            with self.subTest(field=field):
                result = check({'shots': [{'id': '01', field: '柔和阳光照进室内'}]})
                self.assertEqual(result['status'], 'needs_material')
                self.assertTrue(any('references.scene' in item for item in result['missing']))

    def test_warm_light_text_in_every_picture_field_requires_scene_reference(self):
        for field in ('lighting', 'description', 'visual'):
            with self.subTest(field=field):
                result = check({'shots': [{'id': '01', field: '暖光'}]})
                self.assertEqual(result['status'], 'needs_material')
                self.assertTrue(any('references.scene' in item for item in result['missing']))

    def test_room_subarea_modifier_keeps_the_same_location_identity(self):
        for place in ('卧室窗边', '卧室床边', '卧室角落'):
            with self.subTest(place=place):
                result = check({'references': {'scene': '卧室'}, 'shots': [
                    {'id': '01', 'space': place}]})
                self.assertEqual(result['status'], 'ok')
                self.assertFalse(any(item['category'] == '空间' for item in result['issues']), result)

    def test_documented_wardrobe_space_and_lighting_changes_become_new_baselines(self):
        wardrobe = check({'references': {'character': {'林岚': '深蓝外套'}}, 'shots': [
            {'id': '01', 'character': '林岚穿黑色外套', 'transition': {'character': '林岚换上黑色外套'}},
            {'id': '02', 'character': '林岚穿黑色外套'}]})
        self.assertFalse(any(item['category'] == '角色' for item in wardrobe['issues']), wardrobe)

        location = check({'references': {'scene': '书店门口'}, 'shots': [
            {'id': '01', 'space': '走进咖啡店门口'},
            {'id': '02', 'space': '咖啡店门口'}]})
        self.assertFalse(any(item['category'] == '空间' for item in location['issues']), location)

        lighting = check({'references': {'scene': '暖光从左侧'}, 'shots': [
            {'id': '01', 'lighting': '冷光从右侧', 'transition': {'lighting': '重新布光，冷光从右侧'}},
            {'id': '02', 'lighting': '冷光从右侧'}]})
        self.assertFalse(any(item['category'] == '光线' for item in lighting['issues']), lighting)

    def test_new_baseline_does_not_hide_a_later_undocumented_change(self):
        result = check({'references': {'character': {'林岚': '深蓝外套'}}, 'shots': [
            {'id': '01', 'character': '林岚穿黑色外套', 'transition': {'character': '林岚换上黑色外套'}},
            {'id': '02', 'character': '林岚穿黑色外套'},
            {'id': '03', 'character': '林岚穿红色外套'}]})
        role_issues = [item for item in result['issues'] if item['category'] == '角色']
        self.assertTrue(any(item['shots'][-1] == '03' and '红外套' in item['evidence'] for item in role_issues), result)

    def test_ambiguous_multi_person_phone_colors_and_hands_request_attribution(self):
        result = check({'references': {'character': {'林岚': '深蓝外套', '陈默': '白色外套'}}, 'shots': [
            {'id': '01', 'character': '林岚和陈默同框', 'prop': '红色手机、蓝色手机；左手、右手'}]})
        self.assertEqual(result['status'], 'needs_material')
        self.assertTrue(any('标注各道具持有人及左右手' in item for item in result['missing']), result)
        self.assertEqual(result['issues'], [])

    def test_named_holders_keep_distinct_phone_colors_and_hand_sides(self):
        wording = '林岚右手拿红色手机；陈默左手拿蓝色手机'
        result = check({'references': {'character': {'林岚': '深蓝外套', '陈默': '白色外套'}}, 'shots': [
            {'id': '01', 'character': '林岚和陈默同框', 'prop': wording},
            {'id': '02', 'character': '林岚和陈默同框', 'prop': wording}]})
        self.assertEqual(result['status'], 'ok', result)
        self.assertFalse(any(item['category'] == '道具' for item in result['issues']), result)

    def test_venue_adjective_does_not_change_location_identity(self):
        result = check({'references': {'scene': '书店门口'}, 'shots': [
            {'id': '01', 'space': '林岚在安静的书店门口面向右'}]})
        self.assertEqual(result['status'], 'ok')
        self.assertFalse(any(item['aspect'] == '地点' for item in result['issues']), result)

    def test_multi_person_wardrobe_is_compared_across_shots(self):
        result = check({'references': {'character': {'林岚': '深蓝外套', '陈默': '白色外套'}}, 'shots': [
            {'id': '01', 'character': '林岚穿深蓝外套，陈默穿白色外套'},
            {'id': '02', 'character': '林岚穿白色外套，陈默穿黑色外套'}]})
        self.assertEqual(result['status'], 'ok')
        evidence = [item['evidence'] for item in result['issues'] if item['category'] == '角色']
        self.assertEqual(len(evidence), 2)
        self.assertTrue(any('林岚：深蓝外套 → 白外套' in item for item in evidence))
        self.assertTrue(any('陈默：白外套 → 黑外套' in item for item in evidence))

    def test_handoff_sides_are_compared_for_same_prop(self):
        kinds, result = self.categories({'references': {'character': {'林岚': '深蓝外套'}}, 'shots': [
            {'id': '01', 'character': '林岚穿深蓝外套', 'prop': '右手拿黄色纸袋'},
            {'id': '02', 'character': '林岚穿深蓝外套', 'prop': '左手拿黄色纸袋'}]})
        self.assertIn('道具', kinds)
        self.assertTrue(any(item['aspect'] == '纸袋持有手侧' for item in result['issues']))

    def test_unrelated_prop_action_does_not_explain_hand_change(self):
        kinds, result = self.categories({'references': {'character': {'林岚': '深蓝外套'}}, 'shots': [
            {'id': '01', 'character': '林岚穿深蓝外套', 'prop': '右手拿黄色纸袋'},
            {'id': '02', 'character': '林岚穿深蓝外套', 'prop': '拿起手机，左手拿黄色纸袋'}]})
        self.assertIn('道具', kinds)
        self.assertTrue(any(item['aspect'] == '纸袋持有手侧' for item in result['issues']))

    def test_issues_sorted_by_severity(self):
        kinds, result = self.categories({'references': REF, 'shots': [
            {'id': '01', 'character': '林岚穿深蓝外套', 'prop': '右手拿纸袋', 'space': '书店门口面向右'},
            {'id': '02', 'character': '林岚穿白色外套', 'prop': '双手空着', 'space': '书店门口面向左'}]})
        rank = {'high': 0, 'medium': 1, 'low': 2}
        self.assertEqual([rank[x['severity']] for x in result['issues']], sorted(rank[x['severity']] for x in result['issues']))
        self.assertIn('high', {item['severity'] for item in result['issues']})

    def test_severity_changes_with_visual_impact(self):
        result = check({'references': {
            'character': {'林岚': '深蓝外套'},
            'scene': '明亮暖光从左侧，办公室',
        }, 'shots': [
            {'id': '01', 'character': '林岚穿深蓝外套', 'prop': '右手拿手机', 'lighting': '明亮暖光从左侧', 'space': '办公室'},
            {'id': '02', 'character': '林岚穿白色外套', 'prop': '手机在桌上', 'lighting': '昏暗暖光从左侧', 'space': '办公室'},
        ]})
        severity_by_aspect = {item['aspect']: item['severity'] for item in result['issues']}
        self.assertEqual(severity_by_aspect.get('外套'), 'high', result)
        self.assertEqual(severity_by_aspect.get('手机位置'), 'medium', result)
        self.assertEqual(severity_by_aspect.get('光线明暗'), 'low', result)

    def test_negated_actor_states_keep_the_real_name_and_honor_eye_removal(self):
        for wording in ('林岚未戴围巾', '林岚不戴眼镜'):
            with self.subTest(wording=wording):
                self.assertEqual(named_actors(wording), ['林岚'])
        result = check({'references': {'character': {'林岚': '戴黑框眼镜'}}, 'shots': [
            {'id': '01', 'character': '林岚摘下黑框眼镜，未戴眼镜',
             'transition': {'character': '林岚摘下黑框眼镜'}}]})
        self.assertEqual(result['status'], 'ok')
        self.assertFalse(result['issues'], result)

    def test_removed_accessory_becomes_the_later_character_baseline(self):
        result = check({'references': {'character': {'林岚': '红围巾'}}, 'shots': [
            {'id': '01', 'character': '林岚戴红围巾'},
            {'id': '02', 'character': '林岚摘下围巾，未戴围巾',
             'transition': {'character': '林岚摘下围巾'}},
            {'id': '03', 'character': '林岚戴红围巾'},
        ]})
        conflicts = [item for item in result['issues'] if item['category'] == '角色' and item['aspect'] == '围巾']
        self.assertTrue(any(item['shots'] == ['02', '03'] for item in conflicts), result)

    def test_switching_lights_explains_brightness_in_both_directions(self):
        for before, after in (('昏暗', '开灯后明亮'), ('明亮', '关灯后昏暗')):
            with self.subTest(before=before, after=after):
                result = check({'references': {'scene': before}, 'shots': [
                    {'id': '01', 'lighting': before},
                    {'id': '02', 'lighting': after},
                ]})
                self.assertFalse(any(item['aspect'] == '光线明暗' for item in result['issues']), result)

    def test_different_named_people_do_not_align_same_kind_prop_positions(self):
        result = check({'references': {'character': {'林岚': '深蓝外套', '陈默': '白色外套'}}, 'shots': [
            {'id': '01', 'character': '林岚穿深蓝外套', 'prop': '林岚手持手机'},
            {'id': '02', 'character': '陈默穿白色外套', 'prop': '陈默的手机在桌上'},
        ]})
        self.assertEqual(result['status'], 'ok')
        self.assertFalse(any(item['category'] == '道具' for item in result['issues']), result)

    def test_natural_hand_order_reports_unexplained_held_prop_disappearance(self):
        result = check({'references': {'character': {'林岚': '深蓝外套'}}, 'shots': [
            {'id': '01', 'character': '林岚穿深蓝外套', 'prop': '纸袋在右手'},
            {'id': '02', 'character': '林岚穿深蓝外套', 'prop': '双手空着'},
        ]})
        self.assertTrue(any(item['category'] == '道具' and item['aspect'] == '纸袋' for item in result['issues']), result)

    def test_unlisted_gaze_action_still_requires_named_actor_reference(self):
        result = check({'references': {'scene': '卧室'}, 'shots': [
            {'id': '01', 'description': '近景，林岚凝视窗外'}
        ]})
        self.assertEqual(result['status'], 'needs_material')
        self.assertTrue(any('references.character（林岚' in item for item in result['missing']), result)

    def test_common_scene_nouns_are_not_mistaken_for_named_actors(self):
        for reference, wording in (
            ('林间山顶', '林木摇曳，暖光从左侧'),
            ('山顶', '白云飘动，山顶远景'),
        ):
            with self.subTest(wording=wording):
                result = check({'references': {'scene': reference}, 'shots': [
                    {'id': '01', 'description': wording}
                ]})
                self.assertEqual(result['status'], 'ok')
                self.assertFalse(any('references.character' in item for item in result['missing']), result)

    def test_conflicting_states_across_fields_in_one_shot_are_reported(self):
        result = check({'references': {'character': {'林岚': '深蓝外套'}, 'scene': '书店左侧来光'}, 'shots': [
            {'id': '01', 'character': '林岚穿深蓝外套', 'description': '林岚穿白色外套',
             'lighting': '暖光从左侧，同时补光从右侧'}
        ]})
        self.assertTrue(any(item['category'] == '角色' and item['aspect'] == '外套' for item in result['issues']), result)
        self.assertTrue(any(item['category'] == '光线' and item['aspect'] == '来光方向' for item in result['issues']), result)

    def test_drop_of_one_prop_does_not_explain_another_props_position_change(self):
        result = check({'references': {'character': {'林岚': '深蓝外套'}}, 'shots': [
            {'id': '01', 'character': '林岚穿深蓝外套', 'prop': '右手拿手机，左手拿纸袋'},
            {'id': '02', 'character': '林岚穿深蓝外套', 'prop': '放下纸袋，手机在桌上'},
        ]})
        self.assertTrue(any(item['category'] == '道具' and item['aspect'] == '手机位置' for item in result['issues']), result)

    def test_new_held_prop_after_explicitly_empty_hands_needs_transition(self):
        result = check({'references': {'character': {'林岚': '深蓝外套'}}, 'shots': [
            {'id': '01', 'character': '林岚穿深蓝外套', 'prop': '双手空着'},
            {'id': '02', 'character': '林岚穿深蓝外套', 'prop': '右手拿黄色纸袋'},
        ]})
        self.assertTrue(any(item['category'] == '道具' and item['aspect'] == '纸袋' for item in result['issues']), result)

    def test_prop_only_empty_hands_to_new_held_prop_needs_transition(self):
        result = check({'shots': [
            {'id': '01', 'prop': '双手空着'},
            {'id': '02', 'prop': '右手拿黄色纸袋'},
        ]})
        self.assertTrue(any(item['category'] == '道具' and item['aspect'] == '纸袋' for item in result['issues']), result)

    def test_description_or_visual_can_explain_prop_position_change(self):
        for field in ('description', 'visual'):
            with self.subTest(field=field):
                result = check({'shots': [
                    {'id': '01', field: '右手拿手机'},
                    {'id': '02', field: '把手机放在桌上'},
                ]})
                self.assertFalse(any(item['category'] == '道具' and item['aspect'] == '手机位置' for item in result['issues']), result)

    def test_refusal_and_failed_attempts_do_not_explain_changes(self):
        prop_result = check({'shots': [
            {'id': '01', 'prop': '右手拿纸袋'},
            {'id': '02', 'prop': '双手空着', 'transition': {'prop': '拒绝放下纸袋'}},
        ]})
        self.assertTrue(any(item['category'] == '道具' and item['aspect'] == '纸袋' for item in prop_result['issues']), prop_result)
        space_result = check({'references': {'scene': '书店门口'}, 'shots': [
            {'id': '01', 'space': '书店门口'},
            {'id': '02', 'space': '咖啡店门口', 'transition': {'space': '试图走进咖啡店但失败'}},
        ]})
        self.assertTrue(any(item['category'] == '空间' for item in space_result['issues']), space_result)

    def test_common_study_and_classroom_places_require_scene_reference(self):
        for phrase in ('书房，清晨', '教室，白天'):
            with self.subTest(phrase=phrase):
                result = check({'shots': [{'id': '01', 'visual': phrase}]})
                self.assertEqual(result['status'], 'needs_material', result)
                self.assertTrue(any('references.scene' in item for item in result['missing']), result)

    def test_multi_place_scene_reference_allows_each_named_place(self):
        result = check({'references': {'scene': '卧室、阳台均为本场景'}, 'shots': [
            {'id': '01', 'space': '卧室'},
            {'id': '02', 'space': '卧室'},
        ]})
        self.assertEqual(result['status'], 'ok', result)
        self.assertEqual(result['issues'], [], result)

    def test_multi_place_reference_does_not_create_a_self_comparison(self):
        result = check({'references': {'scene': '卧室、阳台均为本场景'}, 'shots': [
            {'id': '01', 'space': '卧室'},
            {'id': '02', 'space': '卧室'},
        ]})
        self.assertFalse(any(item['shots'] == ['01', '01'] for item in result['issues']), result)

    def test_multi_place_reference_reports_only_an_explicit_outside_place(self):
        result = check({'references': {'scene': '卧室、阳台均为本场景'}, 'shots': [
            {'id': '01', 'space': '厨房'},
        ]})
        place_issues = [item for item in result['issues'] if item['category'] == '空间' and item['aspect'] == '地点']
        self.assertEqual(len(place_issues), 1, result)
        self.assertEqual(place_issues[0]['shots'], ['01'])

    def test_explicit_unseen_person_wording_does_not_require_character_reference(self):
        for wording in ('人物未出镜', '角色未出镜', '人物没有出镜', '角色不出镜'):
            with self.subTest(wording=wording):
                result = check({'shots': [{'id': '01', 'description': wording}]})
                self.assertEqual(result['status'], 'ok', result)
                self.assertFalse(any('references.character' in item for item in result['missing']), result)

    def test_documented_pickup_explains_new_prop_after_empty_hands(self):
        result = check({'references': {'character': {'林岚': '深蓝外套'}}, 'shots': [
            {'id': '01', 'character': '林岚穿深蓝外套', 'prop': '双手空着'},
            {'id': '02', 'character': '林岚穿深蓝外套', 'prop': '右手拿黄色纸袋', 'transition': {'prop': '林岚拿起黄色纸袋'}},
        ]})
        self.assertFalse(any(item['category'] == '道具' and item['aspect'] == '纸袋' for item in result['issues']), result)

if __name__ == '__main__':
    unittest.main()
