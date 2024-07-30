from gameplay.towers.base_tower import Tower # NOQA
from constants import imgs


class Dart(Tower):
    def __init__(self, pos):
        super().__init__(imgs["dart"], 0, 250, 0, pos, (0, 0), "grey 50")
        self.name = "Dart"
        self.buff = "test"


class Ice(Tower):
    def __init__(self, pos):
        super().__init__(imgs["ice"], 2, 300, 0.5, pos, (0, 0), "light blue")
        self.name = "Ice"


class Inferno(Tower):
    def __init__(self, pos):
        super().__init__(imgs["inferno"], 2, 300, 0.5, pos, (imgs["inferno"].get_width()//2, (imgs["inferno"].get_height()//2)-26), "dark red")
        self.name = "Inferno Beam"
