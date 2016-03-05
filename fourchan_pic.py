"""Gets random picture from chosen board"""
from urllib import request, error
from random import randrange
import re

class Info:
    def __init__(self, board, f_format):
        self.board = board.replace('/', '')
        self.board_code = '/{}/'.format(self.board)
        self.f_format = f_format.replace('.', '')
        self.file_format = '.{}'.format(self.f_format)

def open_board(board_c):
    if board_c:
        try:
            return request.urlopen("http://a.4cdn.org/" + board_c + \
                "/threads.json").read().decode('utf-8')
        except error.HTTPError:
            return None

def main(info=['', '']):
    if not info[0]:
        board_list_json = request.urlopen("http://a.4cdn.org/boards.json").read().decode('utf-8')
        board_l = re.findall(r'"board":"(\w+)"', board_list_json)
        information = Info(board_l[randrange(0, len(board_l))], '')
    else:
        information = Info(info[0], info[1])
    if information.board == 'f': #/f/ is causing tons of problems
        return main()
    if information.board in ['s', 'hc', 'hm', 'h', 'e', 'u', 'd', 'y', 'hr', 'gif', 'b', 'aco', \
                            'r', 'r9k', 'pol', 'soc']:
        nsfw = ' [NSFW]'
    else:
        nsfw = ''
    thread_numbers = re.findall(r'"no":(\d+)', open_board(information.board))
    thread = request.urlopen("http://a.4cdn.org" + information.board_code + "thread/" + \
             thread_numbers[randrange(1, len(thread_numbers))] + '.json').read().decode('utf-8')
    picture_time = re.findall(r'"tim":(\d+)', thread)
    picture_ext = re.findall(r'"ext":"(\.\w+)"', thread)
    pictures = [i+j for i, j in list(zip(picture_time, picture_ext))]
    if information.f_format:
        format_list = []
        for index, num in enumerate(picture_ext):
            if index == information.file_format:
                format_list.append(pictures[num])
        if format_list:
            pictures = format_list
    end_str = "https://i.4cdn.org" + information.board_code + \
              pictures[randrange(0, len(pictures))] + nsfw
    return end_str

if __name__ == '__main__':
    print(main())
