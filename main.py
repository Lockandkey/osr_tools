import os
import pickle
import random
from math import sqrt
import tables

bands_path = f'{os.getcwd()}/bands'


def get_random_band_name():

    name_table_plural = ['', 's']

    band_name = random.choice(tables.band_name_table_alpha).replace("_", random.choice(tables.band_name_table_bravo)) + random.choice(
        name_table_plural)
    return band_name


def get_random_npc_name():
    character_name = random.choice(
        [  # todo this really needs to be replaced, api pull fantasynamegenerators maybe?
            'Delbert Peck',
            'Jesse Miranda',
            'Alvin Massey',
            'Daniel Shaffer',
            'Gerard Stuart',
            'Danny Ortega',
            'Walter Maynard',
            'Andre Fry',
            'Chad Gallagher',
            'Manuel Allison',
            'Beatrice Powers',
            'Donna Hensley',
            'Rosie Gallagher',
            'Hattie Ware',
            'Michele Mack',
            'Alicia Sanford',
            'Bridget Taylor',
            'Jennifer Kane',
            'Maria Carver',
            'Zoe Sweeney'
        ])
    return character_name


def get_new_random_hostility():
    prob_position = random.randint(1, 6) + random.randint(1, 6)
    if prob_position < 5:
        new_hostility = random.randint(1, 25)
    elif prob_position > 9:
        new_hostility = random.randint(75, 99)
    else:
        new_hostility = random.randint(25, 75)
    return new_hostility


def get_random_character_class():
    # todo implement expanded lists with proper probability matrix
    return random.choice(tables.character_class_common_list)


class AdventuringBand:
    class Adventurer:
        def __init__(self, character_name=None, character_class=None, character_level=None):
            if character_name is not None:
                self.character_name = character_name
            else:
                self.character_name = get_random_npc_name()

            if character_class is not None:
                self.character_class = character_class
            else:
                self.character_class = get_random_character_class()

            if character_level is not None:
                self.character_level = character_level
            else:
                level = abs(13 - int(sqrt(random.randint(1, 144))))  # todo add a better method

                self.character_level = level

        def __str__(self):
            return f'{self.character_name}, level {str(self.character_level)} {self.character_class}.'

    def __init__(self, name=None, hostile_percent=None, party_size=None):
        if name is None:
            self.band_name = get_random_band_name()
        else:
            self.band_name = name

        if hostile_percent is None:
            self.hostility = get_new_random_hostility()
        else:
            self.hostility = hostile_percent

        if party_size is None:
            self.party_size = random.randint(1, 6) + random.randint(1, 6)
        else:
            self.party_size = party_size

        self.party_members = self.generate_party_members()

    def generate_party_members(self):
        party_list = []
        for i in range(self.party_size):
            party_list.append(self.Adventurer())

        return party_list

    def __str__(self):
        return f'Band: {self.band_name}. {str(self.party_size)} members, not including hirelings. Probability of conflict: {self.hostility}%'

    def print_full_details(self):
        text = f'Band name: {self.band_name}\n' \
               f'Hostility: {self.hostility}%\n' \
               f'Party size: {self.party_size}, not including hirelings.'
        for member in self.party_members:
            text = f'{text}\n\t{str(member)}'

        print(text)

    def check_hostile(self):
        if self.hostility < random.randint(1, 100):
            return True
        else:
            return False


def write_existing_bands(list_of_bands):
    with open(bands_path, 'wb') as f:
        pickle.dump(list_of_bands, f)


def read_existing_bands():
    with open(bands_path, 'rb') as f:
        list_of_bands = pickle.load(f)

    return list_of_bands


def band_wilderness_encounter(adventuring_band):
    if random.randint(1, 100) < 75:
        encounter_text = random.choice(tables.wilderness_encounter_evidence_results)
    else:
        if adventuring_band.check_hostile():
            encounter_text = random.choice(tables.wilderness_encounter_direct_hostile_results)
        else:
            encounter_text = random.choice(tables.wilderness_encounter_direct_friendly_results)

    encounter_text.replace("$bandname", adventuring_band.band_name)

    return encounter_text


bands_list = [AdventuringBand()]
write_existing_bands(bands_list)

bands_list = read_existing_bands()

for band in bands_list:
    band.print_full_details()
