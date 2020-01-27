from constants import EPOCHS
from functions import generate_initial_Q, train, play_game, convert_csv_to_Q

file_path = 'pickled_brain2.csv'
pickled_Q = convert_csv_to_Q(file_path)
# print(pickled_Q)
# play
print("Let's play!\n")
play_game(pickled_Q)
print("\nThanks for playing!")
