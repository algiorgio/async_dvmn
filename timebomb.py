import asyncio
import time


class EventLoopCommand:
    def __await__(self):
        return (yield self)


class Sleep(EventLoopCommand):
    def __init__(self, seconds):
        self.seconds = seconds


def convert_seconds_to_iterations(seconds):
    return seconds * 1_000_000


async def do_ticking(amount_of_ticks, sound):
    for _ in range(amount_of_ticks):
        print(sound)
        await Sleep(1)


async def bang_the_bomb(amount_of_ticks=5, sound='tick', bang_sound='boom!'):
    clock = do_ticking(amount_of_ticks, sound)
    await clock
    print(bang_sound)


waiting_bombs = {
    bang_the_bomb(amount_of_ticks=9, sound='click'): 0,
    bang_the_bomb(amount_of_ticks=5, sound='tap', bang_sound='babah!'): 0,
    bang_the_bomb(amount_of_ticks=3, bang_sound='greeet!'): 0
}


while waiting_bombs:
    for bomb in list(waiting_bombs):
        try:
            if waiting_bombs[bomb] <= 0:
                timeout = bomb.send(None).seconds
                ticks_to_sleep = convert_seconds_to_iterations(timeout)
                waiting_bombs[bomb] = ticks_to_sleep
            waiting_bombs[bomb] -= 1
        except StopIteration:
            waiting_bombs.pop(bomb)

# bomb1 = bang_the_bomb(amount_of_ticks=9, sound='click')
# bomb2 = bang_the_bomb(amount_of_ticks=5, sound='tap', bang_sound='babah!')
# bomb3 = bang_the_bomb(amount_of_ticks=3, bang_sound='greeet!')
#
# timer1 = 0
# timer2 = 0
# timer3 = 0
#
#
# while True:
#     try:
#         if timer1 <= 0:
#             timer1 = bomb1.send(None).seconds
#             ticks_to_sleep = convert_seconds_to_iterations(timer1)
#             timer1 = ticks_to_sleep
#         timer1 -= 1
#
#         if timer2 <= 0:
#             timer2 = bomb2.send(None).seconds
#             ticks_to_sleep = convert_seconds_to_iterations(timer2)
#             timer2 = ticks_to_sleep
#         timer2 -= 1
#
#         if timer3 <= 0:
#             timer3 = bomb3.send(None).seconds
#             ticks_to_sleep = convert_seconds_to_iterations(timer3)
#             timer3 = ticks_to_sleep
#         timer3 -= 1
#
#     except StopIteration:
#         break
