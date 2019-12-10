import asyncio
import time
import curses


TIC_TIMEOUT = 0.1


def blink_old(canvas):
    while True:
        try:
            canvas.refresh()
            canvas.border()
            curses.curs_set(False)

            row, column = (5, 20)

            canvas.addstr(row, column, '*', curses.A_DIM)
            time.sleep(2)
            canvas.refresh()

            canvas.addstr(row, column, '*')
            time.sleep(0.3)
            canvas.refresh()

            canvas.addstr(row, column, '*', curses.A_BOLD)
            time.sleep(0.5)
            canvas.refresh()

            canvas.addstr(row, column, '*')
            time.sleep(0.3)
            canvas.refresh()
        except KeyboardInterrupt:
            raise


async def blink(canvas, row, col, symbol='*'):
    while True:
        canvas.refresh()
        canvas.border()
        curses.curs_set(False)

        canvas.addstr(row, col, symbol, curses.A_DIM)
        canvas.refresh()
        await asyncio.sleep(0)

        canvas.addstr(row, col, symbol)
        canvas.refresh()
        await asyncio.sleep(0)

        canvas.addstr(row, col, symbol, curses.A_BOLD)
        canvas.refresh()
        await asyncio.sleep(0)

        canvas.addstr(row, col, symbol)
        canvas.refresh()
        await asyncio.sleep(0)


def draw(canvas, row, col):
    cor_list = []

    for x in range(1, 10, 2):
        cor_list.append(blink(canvas, row, x))

    while True:
        for coroutine in cor_list:
            try:
                coroutine.send(None)
            except StopIteration:
                break
        time.sleep(0.1)


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw, 5, 5)
