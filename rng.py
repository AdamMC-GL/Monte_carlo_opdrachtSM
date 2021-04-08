import time


class Simulation:
    """A monte carlo simulation to simulate the chances of 5 soccer clubs playing
    against one another, higher sample_size for better results"""

    def __init__(self, sample_size, seed=time.time()):
        self.seed = seed  # System time is used as the first seed if no seed is given.
        self.sample_size = sample_size
        self.outcomes = {
            "Ajax":       [0, 0, 0, 0, 0],
            "Feyenoord":  [0, 0, 0, 0, 0],
            "PSV":        [0, 0, 0, 0, 0],
            "FC Utrecht": [0, 0, 0, 0, 0],
            "Willem II":  [0, 0, 0, 0, 0],
        }

        # Game outcome percentage chances (win, tie, lose) for home club
        self.chances = [[[], [65, 17, 18], [54, 21, 25], [74, 14, 12], [78, 13, 9]],
                       [[30, 21, 49], [], [37, 24, 39], [51, 22, 27], [60, 21, 19]],
                       [[39, 22, 39], [54, 22, 24], [], [62, 20, 18], [62, 22, 16]],
                       [[25, 14, 61], [37, 23, 40], [29, 24, 47], [], [52, 23, 25]],
                       [[17, 18, 65], [20, 26, 54], [23, 24, 53], [37, 25, 38], []]]

    def __lcg(self, m):
        """Using the Linear congruential generator to generate
         a random number between 0 and m, m is amplified for better random
         results"""
        a = 1140671482
        c = 128201162
        m = m*10000000
        self.seed = (a*self.seed + c) % m
        return int(self.seed/10000000)

    def __calc_win_percentage(self):
        """This function turns the results for the simulation into the chance of a result happening,
        the results contain how often a team placed 1st though 5th, which is used to determine how
        likely that team is to be placed in said place"""
        for i in self.outcomes:
            for j in range(len(self.outcomes[i])):
                self.outcomes[i][j] = round((self.outcomes[i][j] / self.sample_size * 100), 2)

    def __calc_places(self, scores):
        """This function turns the results of one game into how the teams placed. The team with
        the most points gets 1st place, second most 2nd place, etc"""
        scores_in_order = sorted(scores, key=lambda x: x[1], reverse=True)
        for i, value in enumerate(scores_in_order):
            self.outcomes[value[0]][i] += 1

    def __calc_scores_single_game(self):
        """This function plays a single game. Calculates and returns a list of scores for one
        game. A win is based on the win chance in 'self.chances'. A win gives 3 points, a tie 1 point
        each team."""

        scores = [["Ajax", 0], ["Feyenoord", 0], ["PSV", 0], ["FC Utrecht", 0], ["Willem II", 0]]

        for i in range(len(self.chances)):  # row
            for j in range(len(self.chances[i])):  # column
                win_chance = self.chances[i][j]
                if i != j:  # if column and row are the same the club would play against itself
                    randomNr = self.__lcg(100) + 1  # a random number between 0 and 100
                    if randomNr < win_chance[0]:
                        scores[i][1] += 3
                    elif randomNr > 100 - win_chance[1]:
                        scores[i][1] += 1
                        scores[j][1] += 1
                    else:
                        scores[j][1] += 3
        return scores

    def run_sim(self):
        """The main function, only this function is callable outside the class, this function
        runs the entire simulation. First calculates the scores of a whole tournament, then
        places each team, run for 'sample_size' amount, output is a dict of how many times each
        team placed 1st - 5th, then calculates the win percentage."""
        for run in range(self.sample_size):
            scores = self.__calc_scores_single_game()
            self.__calc_places(scores)
        self.__calc_win_percentage()

    def __str__(self):
        """Returns a string that tells the results of the simulation in a more
        human readable language and proper sentencing"""
        str = ""
        for i in self.outcomes:
            str += f"{i} heeft "
            for j in range(len(self.outcomes[i])):
                str += f"{self.outcomes[i][j]}% kans op {j+1}e plaats "
            str += "\n"
        return str


if __name__ == "__main__":
    sample_size = 20000
    sim = Simulation(sample_size, seed=20)  # if no seed is given, system time is used
    sim.run_sim()
    print(sim)
