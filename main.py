import sys
import pygame
import random
import math

import logic
import shapes
import interactable_objects

pygame.init()
pygame.font.init()

palette = {
    'black': (0, 0, 0),
    'white': (255, 255, 255),
    'blue': (0, 150, 255),
    'light cray': (180, 180, 180),
    'dark cray': (80, 80, 80)
}

fonts = {
    'comicsans': pygame.font.SysFont('comicsansms', 12)
}

logics = ['StepLogic', 'RandomLogic']


class App:
    def __init__(self):
        # Setting the dimensions of the window
        self.size = width, height = 640, 480
        self.border_left = 10
        self.border_right = 200
        self.border_down = 30
        self.border_up = 10
        self.frame = width + self.border_left + self.border_right, height + self.border_up + self.border_down

        # input
        self.input = []
        menu_x = self.size[0] + self.border_left + 10
        menu_y = self.border_up
        input_width = self.border_right - 20
        input_height = 30
        input_space = 10

        self.run_calculator = False     # stop - continue : bool
        self.my_logic = logics[0]

        # mouse
        self.mouse = ((0, 0), (0, 0, 0))

        # general information about the checkpoints
        self.checkpoints = []
        self.number_of_points = 6
        self.pointSize = 6
        self.max_permutations = 0  # self.generate_points gives it the right value

        # constructing the screen
        self.screen = pygame.display.set_mode(self.frame)

        # generate random points & execute self.start()
        self.generate_points()

        # constructing Interface objects
        # progressbar
        self.progressbar = shapes.Progressbar(self.screen,
                                              self.border_left, height + self.border_up + 5,
                                              self.frame[0] - 20, self.border_down - 15,
                                              palette['blue'])



        # pause - continue
        self.input.append(interactable_objects.ToggleButton(
            self.screen,
            menu_x, menu_y, input_width, input_height,
            (palette['dark cray'], palette['dark cray']),
            ('PAUSE', 'START'), fonts['comicsans'], (self.pause_clalc, self.continue_clalc)
        ))
        # restart
        self.input.append(interactable_objects.Button(
            self.screen,
            menu_x, menu_y + 1*(input_height + input_space), input_width, input_height,
            palette['dark cray'], 'RESTART', fonts['comicsans'], self.start
        ))
        # logic choice
        self.input.append(interactable_objects.DropDownMenu(
            self.screen,
            menu_x, menu_y + 2*(input_height + input_space), input_width, input_height,
            (palette['dark cray'],) * 2,
            ('Do all Permutations', 'Make random Changes'),
            fonts['comicsans'], (self.set_to_StepLogic, self.set_to_RandomLogic),
            (None, None), 0
        ))
        #
        self.input.append(interactable_objects.DropDownMenu(
            self.screen,
            menu_x, menu_y + 3*(input_height + input_space), input_width, input_height,
            (palette['dark cray'],)*8,
            ('3', '4', '5', '6', '7', '8', '9', '10'),
            fonts['comicsans'], (self.set_number_of_checkpoints,)*8,
            (3, 4, 5, 6, 7, 8, 9, 10), 4
        ))
        # generate new points
        self.input.append(interactable_objects.Button(
            self.screen,
            menu_x, menu_y + 4*(input_height + input_space), input_width, input_height,
            palette['dark cray'],
            'new points',
            fonts['comicsans'], self.generate_points
        ))
        # counter
        self.input.append(interactable_objects.Counter(
            self.screen,
            menu_x, self.frame[1] - self.border_down - input_height, input_width, input_height,
            palette['dark cray'], ('Permutations', str(self.permutation_counter)), fonts['comicsans']
        ))

        # gameloop
        while True:
            # listening for closing event
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse = (pygame.mouse.get_pos(), pygame.mouse.get_pressed())
                    for i in self.input:
                        if isinstance(i, interactable_objects.DropDownMenu) and i.selected:
                            if self.mouse[1][0]:
                                i.get_clicked(self.mouse[0])
                                self.mouse = ((0, 0), (0, 0, 0))
                    for i in self.input:
                        if self.mouse[0][1]:
                            i.get_clicked(self.mouse[0])

            # update if necessary
            if (self.permutation_counter < self.max_permutations or self.my_logic != logics[0]) and self.run_calculator:
                self.update()

            # draw new frame
            self.draw()
            pygame.display.flip()

    # next step in the logic
    def update(self):
        self.permutation_counter += 1
        self.logic.next_permutation()

        for obj in self.input:
            if isinstance(obj, interactable_objects.Counter):
                obj.change_label(str(self.permutation_counter))

    def draw(self):
        # background
        self.screen.fill(palette['white'])

        # point-field
        pygame.draw.rect(self.screen, palette['dark cray'], (10, 10, self.size[0], self.size[1]), 2)

        # progressbar
        if self.my_logic == logics[0]:
            self.progressbar.draw(self.permutation_counter/self.max_permutations)

        # Input
        for i in self.input:
            i.draw()

        # selected Dropdown
        for i in self.input:
            if isinstance(i, interactable_objects.DropDownMenu) and i.selected:
                i.draw()

        # connection lines
        pygame.draw.lines(self.screen, palette['light cray'], True, self.logic.shortest_way, 1)

        # points
        for point in self.logic.current_permutation:
            pygame.draw.polygon(self.screen, palette['blue'], [(point[0] + self.pointSize, point[1]),
                                                               (point[0]                  , point[1] + self.pointSize),
                                                               (point[0] - self.pointSize , point[1]),
                                                               (point[0]                  , point[1] - self.pointSize)])
    def pause_clalc(self):
        self.run_calculator = False

    def continue_clalc(self):
        self.run_calculator = True

    def set_to_StepLogic(self):
        self.my_logic = logics[0]
        self.start()

    def set_to_RandomLogic(self):
        self.my_logic = logics[1]
        self.start()

    def set_number_of_checkpoints(self, number):
        self.number_of_points = number
        self.generate_points()
        self.start()

    def start(self):
        if self.my_logic == logics[0]:
            self.logic = logic.StepLogic(self.checkpoints)
        elif self.my_logic == logics[1]:
            self.logic = logic.RandomLogic(self.checkpoints)
        self.permutation_counter = 1
        for obj in self.input:
            if isinstance(obj, interactable_objects.Counter):
                obj.change_label(str(self.permutation_counter))

    def generate_points(self):
        print('Here are your new points')
        self.max_permutations = math.factorial(self.number_of_points)
        self.checkpoints = []
        for i in range(self.number_of_points):
            self.checkpoints.append(
                [random.randrange(self.size[0]) + self.border_left, random.randrange(self.size[1]) + self.border_up])
        self.start()

if __name__ == '__main__':
    app = App()
