import os
import pickle
import random

bands_path = f'{os.getcwd()}/bands'
band_list = []


def assign_new_random_hostility():
    prob_position = random.randint(1, 6) + random.randint(1, 6)
    if prob_position < 5:
        new_hostility = random.randint(1, 25)
    elif prob_position > 9:
        new_hostility = random.randint(75, 99)
    else:
        new_hostility = random.randint(25, 75)
    return new_hostility


class AdventuringBand:
    band_name = ""
    hostility = 50

    def __init__(self, name, hostile_percent=0):
        self.band_name = name
        self.hostility = hostile_percent
        if self.hostility == 0:
            self.hostility = assign_new_random_hostility()

    def __str__(self):
        return f'Band: {self.band_name}. Probability of conflict: {self.hostility}'


def write_existing_bands(list_of_bands):
    with open(bands_path, 'wb') as f:
        pickle.dump(list_of_bands, f)


def read_existing_bands():
    with open(bands_path, 'rb') as f:
        list_of_bands = pickle.load(f)

    return list_of_bands


bands_list = [AdventuringBand("Saga"), AdventuringBand("Edda")]

write_existing_bands(bands_list)
read_list = read_existing_bands()

print(f'Randomly selected {random.choice(read_list)}')
