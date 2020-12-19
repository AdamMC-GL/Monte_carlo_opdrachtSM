import time


def lcg(seed, m):
    """Using the Linear congruential generator to generate
     a random number between 0 and m"""
    a = 1140671482
    c = 128201162
    m = m*10000
    for i in range(2000):  # Loop to get a less predictable outcome and give a Time based seed time to update.
        seed = (a*seed + c) % m
    return int(seed/10000)


def monte_carlo(sample_size):
    """A monte carlo simulation to simulate the chances of 5 soccer clubs playing
    against one another, higher sample_size for better resulsts"""
                # 1e 2e 3e 4e 5e
    outcomes = [[0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0]]

    # Game outcome percentage chances (win, tie, lose) for home club
    chances = [[[], [65, 17, 18], [54, 21, 25], [74, 14, 12], [78, 13, 9]],
               [[30, 21, 49], [], [37, 24, 39], [51, 22, 27], [60, 21, 19]],
               [[39, 22, 39], [54, 22, 24], [], [62, 20, 18], [62, 22, 16]],
               [[25, 14, 61], [37, 23, 40], [29, 24, 47], [], [52, 23, 25]],
               [[17, 18, 65], [20, 26, 54], [23, 24, 53], [37, 25, 38], []]]

    # Running the game with their probabilities
    for run in range(sample_size):
        scores = [0, 0, 0, 0, 0]  # order = Ajax, FN, PSV, FCU, W2
        for i in range(len(chances)):
            for j in range(len(chances[i])):
                win_chance = chances[i][j]
                if i != j:  # if column and row are the same the club would play against itself
                    randomNr = lcg(time.time(), 100) + 1  # System time is used as the seed.
                    if randomNr < win_chance[0]:
                        scores[i] += 3
                    elif randomNr > 100 - win_chance[1]:
                        scores[i] += 1
                        scores[j] += 1
                    else:
                        scores[j] += 3

        # Outcome of every game put in the outcomes list
        scores_in_order = sorted(((value, index) for index, value in enumerate(scores)), reverse=True)
        for i in range(len(scores_in_order)):
            outcomes[scores_in_order[i][1]][i] += 1
    return outcomes


sample_size = 5000
results = monte_carlo(sample_size)

# Printing out the results
teams = ["Ajax", "Feyenoord", "PSV", "FC Utrecht", "Willem II"]
for i in range(len(results)):
    print(teams[i] + " heeft ", end='')
    for j in range(len(results[i])):
        print("{}% kans op {}e plaats".format(results[i][j]/(sample_size/100), j+1), end=", ")
    print("\n", end='')
