from debug.logs import write_to_log

write_to_log("Info", "Program Running")

from gameplay.game_loop import game_loop  # noqa: E402
from gameplay.multiplayer.game_client import start_multiplayer # noqa: E402
from ui.main_menu.main import main_menu  # noqa: E402
from constants import screen_width, screen_height, update_towers, version, crash_reporter_active  # noqa: E402
from debug.crash_reporter import crash  # noqa: E402
import pygame as p  # noqa: E402


def main():
    p.init()
    screen = p.display.set_mode((screen_width, screen_height), p.NOFRAME)
    p.display.set_caption("Elemental Defense")
    clock = p.time.Clock()
    update_towers()
    write_to_log("Info", f"Starting Elemental Defense v{version}")

    if crash_reporter_active:
        try:
            return_value = main_menu(screen, clock)
        except Exception as e:
            crash(e, "main_menu")
            return

        if return_value[0] == "level":
            try:
                game_loop(screen, clock, return_value[1])
            except Exception as e:
                crash(e, "game_loop")

        elif return_value[0] == "join":
            try:
                start_multiplayer(return_value[1], screen, clock)
            except Exception as e:
                crash(e, "multiplayer_client")

    else:
        return_value = main_menu(screen, clock)

        if return_value[0] == "level":
            game_loop(screen, clock, return_value[1])

        elif return_value[0] == "join":
            start_multiplayer(return_value[1], screen, clock)


if __name__ == '__main__':
    main()
