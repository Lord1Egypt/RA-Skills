#!/usr/bin/env python3
"""
Travel Itinerary Generator
Generate detailed travel itineraries with times, locations, activities, and photo spots
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path


class TravelItineraryGenerator:
    def __init__(self, destination, duration_days, trip_type="romantic"):
        """
        Initialize itinerary generator

        Args:
            destination: Destination
            duration_days: Number of days
            trip_type: Trip type (romantic, adventure, cultural, foodie, leisure)
        """
        self.destination = destination
        self.duration_days = duration_days
        self.trip_type = trip_type

    def generate_day_plan(self, day_num):
        """
        Generate single day plan

        Args:
            day_num: Day number

        Returns:
            Single day activities list
        """
        # Select activities based on destination and trip type
        activities = self._get_activities_by_destination()

        # Assign to different time slots
        day_activities = {
            'day': day_num,
            'date': self._calculate_date(day_num),
            'activities': [
                {
                    'time': '09:00',
                    'name': activities['morning'][day_num % len(activities['morning'])],
                    'location': self._get_location_name(activities['morning'][day_num % len(activities['morning'])]),
                    'description': self._get_activity_description(activities['morning'][day_num % len(activities['morning'])]),
                    'duration': '2-3 hours',
                    'photo_spot': self._get_photo_spot(activities['morning'][day_num % len(activities['morning'])], 'morning')
                },
                {
                    'time': '12:00',
                    'name': 'Lunch Time',
                    'location': self._get_lunch_recommendation(),
                    'description': 'Enjoy local cuisine',
                    'duration': '1.5 hours',
                    'photo_spot': 'Food check-in'
                },
                {
                    'time': '14:00',
                    'name': activities['afternoon'][day_num % len(activities['afternoon'])],
                    'location': self._get_location_name(activities['afternoon'][day_num % len(activities['afternoon'])]),
                    'description': self._get_activity_description(activities['afternoon'][day_num % len(activities['afternoon'])]),
                    'duration': '2-3 hours',
                    'photo_spot': self._get_photo_spot(activities['afternoon'][day_num % len(activities['afternoon'])], 'afternoon')
                },
                {
                    'time': '17:30',
                    'name': activities['evening'][day_num % len(activities['evening'])],
                    'location': self._get_location_name(activities['evening'][day_num % len(activities['evening'])]),
                    'description': self._get_activity_description(activities['evening'][day_num % len(activities['evening'])]),
                    'duration': '2 hours',
                    'photo_spot': self._get_photo_spot(activities['evening'][day_num % len(activities['evening'])], 'sunset')
                },
                {
                    'time': '20:00',
                    'name': activities['night'][day_num % len(activities['night'])],
                    'location': self._get_location_name(activities['night'][day_num % len(activities['night'])]),
                    'description': self._get_activity_description(activities['night'][day_num % len(activities['night'])]),
                    'duration': '2-3 hours',
                    'photo_spot': self._get_photo_spot(activities['night'][day_num % len(activities['night'])], 'night')
                }
            ],
            'tips': self._get_day_tips(day_num)
        }

        return day_activities

    def generate_full_itinerary(self):
        """
        Generate complete itinerary

        Returns:
            Complete itinerary dictionary
        """
        itinerary = {
            'destination': self.destination,
            'duration_days': self.duration_days,
            'trip_type': self.trip_type,
            'created_at': datetime.now().isoformat(),
            'days': []
        }

        for day in range(1, self.duration_days + 1):
            itinerary['days'].append(self.generate_day_plan(day))

        itinerary['summary'] = self._generate_summary()

        return itinerary

    def _get_activities_by_destination(self):
        """Get activity list based on destination"""
        activities_map = {
            'paris': {
                'morning': [
                    'Explore the Louvre',
                    'Visit Eiffel Tower',
                    'Stroll Champs-Elysees',
                    'Wander Montmartre'
                ],
                'afternoon': [
                    'Musee d\'Orsay',
                    'Seine River Cruise',
                    'Sainte-Chapelle',
                    'Explore Le Marais'
                ],
                'evening': [
                    'Eiffel Tower sunset viewing',
                    'Montmartre artist square',
                    'Seine River sunset cruise',
                    'Arc de Triomphe viewing'
                ],
                'night': [
                    'Romantic French dinner',
                    'Moulin Rouge show',
                    'Seine River night cruise',
                    'Latin Quarter bars'
                ]
            },
            'tokyo': {
                'morning': [
                    'Senso-ji Temple visit',
                    'Meiji Shrine',
                    'Tsukiji Market',
                    'Akihabara Electric Town'
                ],
                'afternoon': [
                    'Shibuya Crossing',
                    'TeamLab Borderless',
                    'Shinjuku shopping',
                    'Harajuku fashion district'
                ],
                'evening': [
                    'Tokyo Tower sunset',
                    'Roppongi Hills observation deck',
                    'Sumida River fireworks',
                    'Shinjuku Gyoen'
                ],
                'night': [
                    'Izakaya experience',
                    'Shinjuku Kabukicho',
                    'Ramen tasting',
                    'Ginza night view'
                ]
            },
            'barcelona': {
                'morning': [
                    'Visit Sagrada Familia',
                    'Casa Batllo',
                    'Park Guell',
                    'Gothic Quarter walking'
                ],
                'afternoon': [
                    'La Boqueria Market',
                    'MNAC Art Museum',
                    'Barcelona Beach',
                    'Camp Nou Stadium'
                ],
                'evening': [
                    'Park Guell sunset',
                    'Barcelona Port',
                    'Gothic Old Town',
                    'Montjuic Hill'
                ],
                'night': [
                    'Tapas food tour',
                    'Flamenco show',
                    'Beach night market',
                    'El Born district bars'
                ]
            },
            'new_york': {
                'morning': [
                    'Statue of Liberty',
                    'Central Park cycling',
                    'Brooklyn Bridge walk',
                    'Empire State Building'
                ],
                'afternoon': [
                    'Metropolitan Museum',
                    'Times Square',
                    'High Line Park',
                    'MoMA'
                ],
                'evening': [
                    'Brooklyn sunset',
                    'Empire State Building sunset',
                ],
                'night': [
                    'Broadway musical',
                    'Times Square night view',
                    'Hudson River night cruise',
                    'Jazz bar'
                ]
            },
            'santorini': {
                'morning': [
                    'Oia Village',
                    'Red Beach',
                    'Fira Town',
                    'Akrotiri Ruins'
                ],
                'afternoon': [
                    'Black Beach',
                    'Volcanic island boat tour',
                    'Oia photography',
                    'Wine tasting tour'
                ],
                'evening': [
                    'Oia sunset viewing',
                    'Cliffside restaurant',
                    'Volcanic island sunset',
                    'Fira cliff walking'
                ],
                'night': [
                    'Cliffside romantic dinner',
                    'Stargazing',
                    'Beach bar',
                    'Local seafood dinner'
                ]
            }
        }

        # Default general activities
        default_activities = {
            'morning': ['Explore city landmarks', 'Visit famous attractions', 'City walking tour', 'Market experience'],
            'afternoon': ['Museum visit', 'Shopping experience', 'Attraction exploration', 'Cultural discovery'],
            'evening': ['Sunset viewing', 'City observation deck', 'Riverside/beach walk', 'Historic district'],
            'night': ['Local cuisine', 'Nightlife experience', 'Performance appreciation', 'Romantic dinner']
        }

        return activities_map.get(self.destination.lower(), default_activities)

    def _get_location_name(self, activity_name):
        """Get specific location name for activity"""
        location_map = {
            'Explore the Louvre': 'Musee du Louvre',
            'Visit Eiffel Tower': 'Eiffel Tower',
            'Wander Montmartre': 'Montmartre Hill',
            'Senso-ji Temple visit': 'Senso-ji Temple',
            'TeamLab Borderless': 'TeamLab Borderless',
            'Visit Sagrada Familia': 'Sagrada Familia',
            'Park Guell': 'Park Guell',
            'Statue of Liberty': 'Statue of Liberty',
            'Central Park cycling': 'Central Park',
            'Oia Village': 'Oia Village'
        }
        return location_map.get(activity_name, activity_name)

    def _get_activity_description(self, activity):
        """Get activity description"""
        descriptions = {
            'Explore the Louvre': 'World\'s largest art museum, home to Mona Lisa and countless masterpieces',
            'Visit Eiffel Tower': 'Paris\' iconic landmark, climb to enjoy panoramic views of the city',
            'Senso-ji Temple visit': 'Tokyo\'s oldest temple, experience traditional Japanese culture',
            'TeamLab Borderless': 'Immersive digital art experience with interlaced light and shadow',
            'Visit Sagrada Familia': 'Gaudi\'s unfinished masterpiece, unique architectural art',
            'Park Guell': 'Gaudi-designed colorful mosaic park, panoramic view of Barcelona',
            'Statue of Liberty': 'Symbol of New York freedom, take ferry to see up close',
            'Central Park cycling': 'Manhattan\'s urban oasis, perfect for cycling and picnics',
            'Oia sunset viewing': 'One of the world\'s most beautiful sunsets, blue-domed churches as backdrop'
        }
        return descriptions.get(activity, f'Experience the unique charm of {activity}')

    def _get_photo_spot(self, activity, time_of_day):
        """Get photo check-in spot"""
        if time_of_day == 'morning':
            return f'{activity} check-in - Best morning shooting time'
        elif time_of_day == 'afternoon':
            return f'{activity} unique angle - Beautiful scenery under bright light'
        elif time_of_day == 'sunset':
            return f'{activity} sunset view - Golden hour romantic atmosphere'
        elif time_of_day == 'night':
            return f'{activity} night check-in - Glowing night view'
        return f'{activity} check-in point'

    def _get_lunch_recommendation(self):
        """Get lunch recommendation"""
        lunch_spots = {
            'paris': 'Left Bank cafe',
            'tokyo': 'Tsukiji sushi restaurant',
            'barcelona': 'Tapas bistro',
            'new_york': 'Chelsea Market',
            'santorini': 'Seaview restaurant'
        }
        return lunch_spots.get(self.destination.lower(), 'Local specialty restaurant')

    def _get_day_tips(self, day_num):
        """Get day tips"""
        tips = [
            'Remember to book popular attraction tickets in advance',
            'Stay energized, wear comfortable shoes',
            'Prepare camera and power bank',
            'Learning a few local phrases will be very helpful',
            'Carry a map with you, understand public transportation'
        ]
        return tips[day_num % len(tips)]

    def _calculate_date(self, day_num):
        """Calculate date"""
        start_date = datetime.now() + timedelta(days=7)
        target_date = start_date + timedelta(days=day_num-1)
        return target_date.strftime('%Y-%m-%d')

    def _generate_summary(self):
        """Generate itinerary summary"""
        return {
            'total_activities': self.duration_days * 5,
            'must_visit_spots': self._get_activities_by_destination()['morning'],
            'photo_opportunities': self.duration_days * 4,
            'estimated_budget': f'${self.duration_days * 150} - ${self.duration_days * 300}',
            'best_season': 'Suitable year-round (specific season depends on destination)'
        }


def save_itinerary_to_file(itinerary, output_file="travel_itinerary.json"):
    """
    Save itinerary to file

    Args:
        itinerary: Itinerary dictionary
        output_file: Output file path
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(itinerary, f, indent=2, ensure_ascii=False)

    print(f"✅ Itinerary saved to: {output_file}")
    print(f"📅 Days: {itinerary['duration_days']}")
    print(f"📍 Destination: {itinerary['destination']}")
    print(f"📊 Total activities: {itinerary['summary']['total_activities']}")


def print_itinerary_summary(itinerary):
    """Print itinerary summary"""
    print(f"\n{'='*80}")
    print(f"🌍 Travel Itinerary: {itinerary['destination']}")
    print(f"{'='*80}")
    print(f"📅 Days: {itinerary['duration_days']} days")
    print(f"❤️  Type: {itinerary['trip_type']}")
    print(f"📊 Total activities: {itinerary['summary']['total_activities']}")
    print(f"📸 Photo opportunities: {itinerary['summary']['photo_opportunities']} times")
    print(f"💰 Budget: {itinerary['summary']['estimated_budget']}")
    print(f"{'='*80}\n")

    for day in itinerary['days']:
        print(f"Day {day['day']} - {day['date']}")
        print("-" * 80)
        for act in day['activities']:
            print(f"  {act['time']} | {act['name']} | 📸 {act['photo_spot']}")
        print()


def main():
    """Command line usage"""
    if len(sys.argv) < 3:
        print("Usage:")
        print("  itinerary_generator.py <destination> <duration_days> [trip_type]")
        print("\nExamples:")
        print("  itinerary_generator.py Paris 5 romantic")
        print("  itinerary_generator.py Tokyo 7 adventure")
        print("  itinerary_generator.py Barcelona 4 cultural")
        sys.exit(1)

    destination = sys.argv[1]
    duration = int(sys.argv[2])
    trip_type = sys.argv[3] if len(sys.argv) > 3 else "romantic"

    generator = TravelItineraryGenerator(destination, duration, trip_type)
    itinerary = generator.generate_full_itinerary()

    # Save to file
    output_file = f"{destination.lower()}_itinerary_{duration}days.json"
    save_itinerary_to_file(itinerary, output_file)

    # Print summary
    print_itinerary_summary(itinerary)


if __name__ == "__main__":
    main()
