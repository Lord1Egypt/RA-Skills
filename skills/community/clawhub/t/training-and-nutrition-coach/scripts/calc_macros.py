#!/usr/bin/env python3
import argparse, json

def activity_factor(level: str) -> float:
    mapping = {
        'sedentary': 1.2,
        'light': 1.375,
        'moderate': 1.55,
        'high': 1.725,
        'very_high': 1.9,
    }
    return mapping.get(level, 1.55)

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--sex', choices=['male','female'], default='male')
    p.add_argument('--age', type=int, required=True)
    p.add_argument('--height-cm', type=float, required=True)
    p.add_argument('--weight-kg', type=float, required=True)
    p.add_argument('--activity', default='moderate')
    p.add_argument('--goal', choices=['fat_loss','muscle_gain','recomp','maintenance'], default='maintenance')
    args = p.parse_args()

    if args.sex == 'male':
        bmr = 10 * args.weight_kg + 6.25 * args.height_cm - 5 * args.age + 5
    else:
        bmr = 10 * args.weight_kg + 6.25 * args.height_cm - 5 * args.age - 161

    maintenance = bmr * activity_factor(args.activity)

    if args.goal == 'fat_loss':
        calories = maintenance - 350
        protein = 2.0 * args.weight_kg
        fats = 0.8 * args.weight_kg
    elif args.goal == 'muscle_gain':
        calories = maintenance + 250
        protein = 1.8 * args.weight_kg
        fats = 0.8 * args.weight_kg
    elif args.goal == 'recomp':
        calories = maintenance - 100
        protein = 2.0 * args.weight_kg
        fats = 0.8 * args.weight_kg
    else:
        calories = maintenance
        protein = 1.7 * args.weight_kg
        fats = 0.8 * args.weight_kg

    carbs = max(0, (calories - protein * 4 - fats * 9) / 4)

    result = {
        'maintenance_kcal': round(maintenance / 50) * 50,
        'target_kcal': round(calories / 50) * 50,
        'protein_g': round(protein / 5) * 5,
        'fat_g': round(fats / 5) * 5,
        'carbs_g': round(carbs / 5) * 5,
    }
    print(json.dumps(result, ensure_ascii=False))

if __name__ == '__main__':
    main()
