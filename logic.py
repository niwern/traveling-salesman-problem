import itertools
import random


class Logic:
    def length_of_way(self):
        past_point = None
        end_point = self.current_permutation[-1]
        start_point = self.current_permutation[0]
        length = ((start_point[0] - end_point[0]) ** 2 + (start_point[1] - end_point[1]) ** 2) ** 0.5
        for current_point in self.current_permutation:
            if past_point is None:
                past_point = current_point
            else:
                length += ((past_point[0] - current_point[0]) ** 2 + (past_point[1] - current_point[1]) ** 2) ** 0.5
                past_point = current_point
        return length


class RandomLogic(Logic):
    def __init__(self, checkpoints):
        self.current_permutation = checkpoints
        self.shortest_way = self.current_permutation
        self.length_of_shortest_way = self.length_of_way()
        self.number_of_points = len(self.current_permutation)

    def next_permutation(self):
        i = random.randrange(self.number_of_points)
        j = random.randrange(self.number_of_points)

        self.__current_permutation[i], self.__current_permutation[j] = self.__current_permutation[j], self.__current_permutation[i]
        if self.length_of_shortest_way > self.length_of_way():
            self.shortest_way = self.current_permutation
            self.length_of_shortest_way = self.length_of_way()

    @property
    def current_permutation(self):
        arr = []
        for elem in self.__current_permutation:
            arr.append(elem)
        return arr

    @current_permutation.setter
    def current_permutation(self, arr):
        self.__current_permutation = arr


class StepLogic(Logic):
    def __init__(self, checkpoints):
        self.all_permutations = itertools.permutations(checkpoints)
        self.shortest_way = self.current_permutation = next(self.all_permutations)
        self.length_of_shortest_way = self.length_of_way()

    def next_permutation(self):
        self.current_permutation = next(self.all_permutations)

        if self.length_of_shortest_way > self.length_of_way():
            self.shortest_way = self.current_permutation
            self.length_of_shortest_way = self.length_of_way()


if __name__ == '__main__':
    log = RandomLogic([(0, 1), (0, 0), (0, 2)])

    for i in range(30):
        log.next_permutation()
        print(log.current_permutation, log.length_of_way())

    print()
    print(log.shortest_way)
    print(log.length_of_shortest_way)
