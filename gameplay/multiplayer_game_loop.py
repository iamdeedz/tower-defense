import pygame as p
from constants import fps, backgrounds, medium_backgrounds, server_manager_ip, calc_scaled_tuple, calc_scaled_num, screen_width, screen_height
from gameplay.levels.waves import waves
from ui.text import draw_text
from ui.shop.shop import Shop
from ui.upgrades import draw_upgrades, update_upgrades, toggle_upgrades
from ui.transfer.transfer import update_transfer, draw_transfer

import asyncio
from pymultiplayer import MultiplayerClient
from json import loads, dumps

other_client_ids = set()
id_to_name = {}
client = None


async def msg_handler(msg):
    msg = loads(msg)
    print(msg)

    match msg["type"]:
        case "client_joined":
            other_client_ids.add(msg["content"])

        case "client_left":
            other_client_ids.remove(msg["content"])

        case "sync":
            pass

        case "name":
            id_to_name[msg["content"]["id"]] = msg["content"]["name"]


async def gamestate_manager(screen, clock, level_id):
    go_to_game = await lobby(screen, clock, level_id)

    if go_to_game:
        await multiplayer_game_loop(screen, clock, level_id)

async def lobby(screen, clock, level_id):
    while True:
        for event in p.event.get():
            if event.type == p.QUIT or (event.type == p.KEYDOWN and event.key == p.K_ESCAPE):
                await client.disconnect()
                quit()

        screen.fill(p.Color("grey 25"))

        # Draw
        margin = calc_scaled_tuple((100, 100))
        clients_rect = p.Rect(margin, (screen_width-(margin[0]*2), screen_height-(margin[1]*2)))
        p.draw.rect(screen, p.Color("grey 50"), clients_rect, border_radius=round(clients_rect.width / calc_scaled_num(25.6)))

        screen.blit(medium_backgrounds[level_id],
                    (clients_rect.left + calc_scaled_num(50), clients_rect.top + calc_scaled_num(50, "vertical")))

        p.display.update()
        clock.tick(fps)

async def multiplayer_game_loop(screen, clock, level_id):
    pass


def start_multiplayer(screen, clock, level_id, port):
    global client
    client = MultiplayerClient(msg_handler, ip=server_manager_ip, port=port)
    client.start()

    asyncio.run(gamestate_manager(screen, clock, level_id))
