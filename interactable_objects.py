import pygame
from shapes import Rect
from main import palette as palette


class Input(Rect):
    def __init__(self, screen, x, y, width, height, color, label, font):
        super(Input, self).__init__(screen, x, y, width, height, color)
        self.label = label
        self.font = font

    def clicked(self, mouse_pos):
        if self.x < mouse_pos[0] < self.x + self.width:
            if self.y < mouse_pos[1] < self.y + self.height:
                return True
        else:
            return False

    def get_clicked(self, mouse_pos):
        if self.clicked(mouse_pos):
            print('~(O.o)~ /Yeah jemand hat mich beachted')

    def move(self, x, y):
        self.x += x
        self.y += y


class Selectable(Input):
    selected = False

    def draw_selected(self):
        raise Exception('Give me purpose!')

    def draw_unselected(self):
        raise Exception('Give me purpose!')

    def draw(self):
        if self.selected:
            self.draw_selected()
        else:
            self.draw_unselected()


class Rewriteable(Input):
    def change_label(self, new_label):
        self.label = new_label


class DropDownMenu(Selectable, Input):
    selected_button: int

    def __init__(self, screen, x, y, width, height, colors, labels, font, actions, parameters, index_selected=0):
        Input.__init__(self, screen, x, y, width, height, colors[0], labels[index_selected], font)
        self.selected_button = index_selected
        if len(colors) != len(labels) or len(labels) != len(actions) or labels == []:
            raise Exception('invalid input. Need more information!')

        self.buttons = []
        height -= 1 # the borders shoud overlap
        for color, name, action, parameter in zip(colors, labels, actions, parameters):
            self.buttons.append(Button(
                screen,
                x, y + height * len(self.buttons),
                width, height,
                color, name, font, action, parameter
            ))

    def get_clicked(self, mouse_pos):
        if self.selected:
            for i, button in enumerate(self.buttons):
                if button.clicked(mouse_pos):
                    button.get_clicked(mouse_pos)
                    self.label = button.label
            self.selected = False
        elif self.clicked(mouse_pos):
            self.selected = True

    def draw_unselected(self):
        pygame.draw.rect(self.screen, self.color, self.get_dimensions(), 1)

        x, y = self.get_middle()
        text = self.font.render(self.label, True, self.color)

        self.screen.blit(text, (x - text.get_width() // 2, y - text.get_height() // 2))

    def draw_selected(self):
        # background plain
        border = 2
        pygame.draw.rect(
            self.screen, palette['white'],
            (self.x - border, self.y - border, self.width + 2 * border, len(self.buttons) * self.height + 2 * border))

        for button in self.buttons:
            button.draw()


class Button(Input):
    def __init__(self, screen, x, y, width, height, color, label, font, action, parameter=None):
        """
        initalizing a Button
        :param screen:
        :param x, y: position of the upper left corner
        :param width, height: dimensions of the closed menu
        :param color: colors of the frame and text, when unselected and selected
        :param label: labels of the (unselected, selected) button
        :param font: pygame.font object for the text
        :param action: function, that gets executed, when pressed
        """
        super(Button, self).__init__(screen, x, y, width, height, color, label, font)
        self.action = action
        self.parameter = parameter

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.get_dimensions(), 1)

        x, y = self.get_middle()
        text = self.font.render(self.label, True, self.color)

        self.screen.blit(text, (x - text.get_width() // 2, y - text.get_height() // 2))

    def get_clicked(self, mouse_pos):
        if self.clicked(mouse_pos):
            print(str(self) + " has been pressed.")
            if self.parameter is not None:
                self.action(self.parameter)
            else:
                self.action()

    def __str__(self):
        return "Button '{}'".format(self.label)


class ToggleButton(Selectable, Button):
    def __init__(self, screen, x, y, width, height, colors, labels, font, actions, parameters=(None, None)):
        super(ToggleButton, self).__init__(screen, x, y, width, height, colors[0], str(labels), font, self.execute_action)
        self.selected_button = Button(screen, x, y, width, height, colors[0], labels[0], font, actions[0], parameters[0])
        self.unselected_button = Button(screen, x, y, width, height, colors[1], labels[1], font, actions[1], parameters[1])

    def draw_selected(self):
        self.selected_button.draw()

    def draw_unselected(self):
        self.unselected_button.draw()

    def execute_action(self):
        if self.selected:
            self.selected_button.get_clicked(mouse_pos)

    def get_clicked(self, mouse_pos):
        if self.clicked(mouse_pos):
            self.selected_button.get_clicked(mouse_pos) if self.selected else self.unselected_button.get_clicked(mouse_pos)
            if self.selected:
                self.selected = False
            else:
                self.selected = True

    def draw(self):
        Selectable.draw(self)


class Text(Input):
    def __init__(self, screen, x, y, width, height, color, label, font):
        super(Text, self).__init__(screen, x, y, width, height, color, label, font)

    def draw(self):
        text = self.font.render(self.label, True, self.color)
        self.screen.blit(text, (self.x, self.y))


class Counter(Rewriteable, Input):
    def __init__(self, screen, x, y, width, height, color, labels, font):
        Rect.__init__(self, screen, x, y, width, height, color)
        self.title = Text(screen, x, y, width, height // 2, color, labels[0], font)
        self.counter = Text(screen, x, y - height // 2, width, height, color, labels[1], font)

    def draw(self):
        self.title.draw()
        self.counter.draw()

    def change_label(self, new_label):
        self.counter.label = new_label
