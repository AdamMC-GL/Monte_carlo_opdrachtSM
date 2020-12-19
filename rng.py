import time

def lcg(rand, m):
    a = 1140671482
    c = 128201162
    m = m*10000
    for i in range(2000):
        rand = (a*rand + c) % m
    return int(rand/10000)

def monte_carlo(sample_size):
                # 1e 2e 3e 4e 5e
    outcomes = [[0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0]]

    chances = [[[], [65, 17, 18], [54, 21, 25], [74, 14, 12], [78, 13, 9]],
               [[30, 21, 49], [], [37, 24, 39], [51, 22, 27], [60, 21, 19]],
               [[39, 22, 39], [54, 22, 24], [], [62, 20, 18], [62, 22, 16]],
               [[25, 14, 61], [37, 23, 40], [29, 24, 47], [], [52, 23, 25]],
               [[17, 18, 65], [20, 26, 54], [23, 24, 53], [37, 25, 38], []]]

    for k in range(sample_size):
        scores = [0, 0, 0, 0, 0]  # order = Ajax, FN, PSV, FCU, W2
        for i in range(len(chances)):
            for j in range(len(chances[i])):
                winchance = chances[i][j]
                if (i != j):
                    randomNr = lcg(time.time(), 100) + 1
                    if randomNr < winchance[0]:
                        scores[i] += 3
                    elif randomNr > 100 - winchance[1]:
                        scores[i] += 1
                        scores[j] += 1
                    else:
                        scores[j] += 3

        orderscores = sorted(((value, index) for index, value in enumerate(scores)), reverse=True)
        for i in range(len(orderscores)):
            outcomes[orderscores[i][1]][i] += 1
    return outcomes


sample_size = 5000
uitslagen = monte_carlo(sample_size)
teams = ["Ajax", "Feyenoord", "PSV", "FC Utrecht", "Willem II"]
for i in range(len(uitslagen)):
    print(teams[i] + " heeft ", end='')
    for j in range(len(uitslagen[i])):
        print("{}% kans op {}e plaats".format(uitslagen[i][j]/(sample_size/100), j+1), end=", ")
    print("\n")