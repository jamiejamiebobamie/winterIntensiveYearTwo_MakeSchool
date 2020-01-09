import random

def check_winner(state):
    """
        Time complexity : O(33)
        Iterates over the board spaces,
        Recording the indices of X's (1) and O's (0) in two sets.

        Iterates through the winning combinations in WINNERS
        to see if there is a winner.

        Returns 1, 0, or -1 if X wins, O wins,
        or if there is a tie, respectively.

        Returns None if there is no winner or tie.

    """

    X = set()
    O = set()

    # O(9)
    for i, board_space in enumerate(state):
        if board_space == 1:
            X.add(i)
        elif board_space == 0:
            O.add(i)

    # O(8*3) = O(24)
    for winner in WINNERS:
        X_count = 0
        O_count = 0
        for w in winner:
            if w in X:
                X_count += 1
            elif w in O:
                O_count += 1
        if X_count == 3:
            return 1 # X wins
        elif O_count == 3:
            return 0 # O wins

    if len(X) + len(O) == len(state):
        return -1 # tie

def generate_initial_Q():
    """
        This builds the initial brain or 'Q'.
        Returns a dictionary of states associated with an array of actions.
        Like longterm memory.

        All actions are set to an intial value of zero.

    """

    states_dictionary = {}

    # log the intial empty board as a state.
    states_dictionary[(None,None,None,None,None,None,None,None,None)] = [0,0,0,
                                                                0,0,0, 0,0,0]
    count = 0
    # one hundred thousand is enough games to generate all states?
    while count < 100000:

        board = [None,None,None,None,None,None,None,None,None]
        Xs_turn = bool(random.getrandbits(1))

        while None in board:

            move_here = pick_random_move(board)

            if Xs_turn:
                board[move_here] = 1
                Xs_turn = False
            else:
                board[move_here] = 0
                Xs_turn = True

            state = tuple(board)

            # log the state and actions
            if state not in states_dictionary:

                # all states of Q should be initialized to 0
                states_dictionary[state] = [0,0,0, 0,0,0, 0,0,0]

        count += 1

    print("Done initializing Q.")
    return states_dictionary # 8953 possible states

def compute_R(state, turn):
    """
        Returns the reward array for the current state.
        "Short term" memory / immediate gratification.

    """
    # sets of indices where X has gone, O has gone, and no one has gone.
    X = set()
    O = set()
    N = set()

    R = [] # possible actions given current state
    for i, board_position in enumerate(state):
        if board_position == None:
            R.append(0)
            N.add(i)
        else:
            R.append(-1)
            if board_position == 1:
                X.add(i)
            else:
                O.add(i)

    X_count = 0
    O_count = 0
    for winner in WINNERS:
        for w in winner:
            if w in X:
                X_count += 1
            elif w in O:
                O_count += 1

    possible_winners = set()
    if X_count >= 2 and turn == True:
        possible_winners = X|N
    elif O_count >= 2 and turn == False:
        possible_winners = O|N

    for i, score in enumerate(R):
        if score == 0:
            if i in possible_winners:
                R[i] = .2

    return R

def pick_random_move(state):
    """
        Determine which indices into the board array contain None.
        These are the possible moves.

        Returns the index into the state array of the next move.

    """

    possible_moves = []
    for i, moves in enumerate(state):
        if moves == None:
            possible_moves.append(i)

    random_index_into_possible_moves = random.randint(0,
                                                len(possible_moves)-1)

    return possible_moves[random_index_into_possible_moves]

def play_tictactoe_turn(state, turn):
    """
        Play a single turn of tic tac toe:
         updates the Q model.
         returns the new board state and the next person's turn.
    """

    action = pick_random_move(state)
    board_state = list(state)

    """

    Q(state, action) =

        R(state, action) + Gamma * Max[Q(next state, all actions)]

    """

    R = compute_R(state,turn)

    Q[state][action] = R[action] + GAMMA * max(Q[state])

    if turn:
        board_state[action] = 1
        turn = False
    else:
        board_state[action] = 0
        turn = True

    new_board_state = tuple(board_state)
    return new_board_state, turn

def test_Q_with_state(Q, state):
    """
        Given a trained brain, Q and a board state:

            (0, 1, 0, 1, None, None, None, None, 0)

        recieve an index in the board state tuple for the suggested next move.

    """

    valid_state = Q.get(state, None)

    if valid_state == None:
        return "Not valid board state."

    winner = check_winner(state)

    if winner != None:
        return "There is already a winner."

    max_index = -1
    max_choice = float("-inf")

    for i, choice in enumerate(Q[state]):

        temp = max_choice
        max_choice = max(max_choice,choice)

        if temp != max_choice:
            max_index = i

    return max_index


# initializing parameters
WINNERS = set()
WINNERS.add((0,1,2))
WINNERS.add((3,4,5))
WINNERS.add((6,7,8))
WINNERS.add((0,3,6))
WINNERS.add((1,4,7))
WINNERS.add((2,5,8))
WINNERS.add((0,4,8))
WINNERS.add((2,4,6))

GAMMA = 0.7
epochs = 1000000

# initializing the brain
Q = generate_initial_Q()

winner = None

# training
for _ in range(epochs):
    board = [None,None,None,None,None,None,None,None,None]
    board_state = tuple(board)

    # X's turn equals True, O's turn equals False
    turn = bool(random.getrandbits(1))

    while winner == None:
        board_state, turn = play_tictactoe_turn(board_state, turn)
        winner = check_winner(board_state)
    else:
        winner = None

print("Done training.")

# testing
rand_state = random.choice(list(Q.keys()))
suggested_index_of_move = test_Q_with_state(Q, rand_state)
print("\nBoard State:")
print(rand_state[:3])
print(rand_state[3:6])
print(rand_state[6:9])
print("\nSuggested next move (0-8):")
print(suggested_index_of_move)

"""

WRONG:

Board State:
(None, 0, 1)
(0, 0, 1)
(None, None, None)

Suggested next move (0-8):
0

"""
