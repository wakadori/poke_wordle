#!/usr/bin/env python3

from enum import IntEnum
import json
import random

class CellState(IntEnum):
    INIT = 0
    MISS = 1
    ORANGE = 2
    GREEN = 3

class Levels(IntEnum):
    DEFAULT = 0
    FIRST = 1
    SECOND = 2
    THIRD = 3
    FOURTH = 4
    FIFTH = 5

class PokeNameManager:
    '''
    回答可能なポケモンリストと、
    答えとなるランダムな1匹を返す。
    '''
    def __init__(self):
        with open('pokelist_five.json', encoding="utf-8") as f:
            self.pokelist_five = json.load(f)
        with open('pokelist.json', encoding="utf-8") as f:
            self.pokelist = json.load(f)

    def get_answer_pokemon(self, level):
        if level == Levels.FIRST:
            return self.pokelist_five["first"][random.randint(0, len(self.pokelist_five["first"])-1)]
        elif level == Levels.SECOND:
            return self.pokelist_five["second"][random.randint(0, len(self.pokelist_five["second"])-1)]
        elif level == Levels.THIRD:
            return self.pokelist_five["third"][random.randint(0, len(self.pokelist_five["third"])-1)]
        elif level == Levels.FOURTH:
            return self.pokelist_five["fourth"][random.randint(0, len(self.pokelist_five["fourth"])-1)]
        elif level == Levels.FIFTH:
            return self.pokelist_five["fifth"][random.randint(0, len(self.pokelist_five["fifth"])-1)]
        elif level == Levels.DEFAULT:
            lists = self.pokelist_five["first"] + self.pokelist_five["second"] + self.pokelist_five["third"] + self.pokelist_five["fourth"]
            return lists[random.randint(0, len(self.pokelist_five["fifth"])-1)]
        else:
            raise Exception

    def get_answerable_pokemons(self, level):
        '''
        現状全てのポケモンを回答可能にしている。
        '''
        return self.pokelist["first"] + self.pokelist["second"] + self.pokelist["third"] + self.pokelist["fourth"] + self.pokelist["fifth"]

class FiftyTable:
    '''
    五十音表
    '''
    def __init__(self):
        self.fifty = {
            "ア": 0,"カ": 0,"サ": 0,"タ": 0,"ナ": 0,"ハ": 0,"マ": 0,"ヤ": 0,"ラ": 0,"ワ": 0,"ガ": 0,"ザ": 0,"ダ": 0,"バ": 0,"パ": 0,"ァ": 0,"ャ": 0,
            "イ": 0,"キ": 0,"シ": 0,"チ": 0,"ニ": 0,"ヒ": 0,"ミ": 0,"ヰ": 1,"リ": 0,"ヵ": 1,"ギ": 0,"ジ": 0,"ヂ": 0,"ビ": 0,"ピ": 0,"ィ": 0,"ュ": 0,
            "ウ": 0,"ク": 0,"ス": 0,"ツ": 0,"ヌ": 0,"フ": 0,"ム": 0,"ユ": 0,"ル": 0,"ヲ": 1,"グ": 0,"ズ": 0,"ヅ": 0,"ブ": 0,"プ": 0,"ゥ": 0,"ョ": 0,
            "エ": 0,"ケ": 0,"セ": 0,"テ": 0,"ネ": 0,"ヘ": 0,"メ": 0,"ヱ": 1,"レ": 0,"ヶ": 1,"ゲ": 0,"ゼ": 0,"デ": 0,"ベ": 0,"ペ": 0,"ェ": 0,"ッ": 0,
            "オ": 0,"コ": 0,"ソ": 0,"ト": 0,"ノ": 0,"ホ": 0,"モ": 0,"ヨ": 0,"ロ": 0,"ン": 0,"ゴ": 0,"ゾ": 0,"ド": 0,"ボ": 0,"ポ": 0,"ォ": 0,"ー": 0,
        }

    def update(self, target, level):
        '''
        target文字の使用状況をlevelで更新する
        '''
        if target in self.fifty.keys():
            if self.fifty[target] < level:
                self.fifty[target] = level

    def updates(self, target_cells):
        '''
        target_cellsのstateを用いて更新する。
        '''
        for cell in target_cells:
            self.update(cell.char, cell.state)

    def show_fifty(self):
        '''
        五十音表を良い感じに表示する
        '''
        c = 0
        for item, value in self.fifty.items():
            if item in ["ヰ","ヱ","ヵ","ヲ","ヶ"]:
                print('\033[8m'+f'{item}'+'\033[0m', end='')
            elif value == CellState.INIT:
                print(item, end="")
            elif value == CellState.ORANGE:
                print('\033[33m'+f'{item}'+'\033[0m', end='')
            elif value == CellState.GREEN:
                print('\033[32m'+f'{item}'+'\033[0m', end='')
            else:
                print('\033[2m'+f'{item}'+'\033[0m', end='')
            c += 1
            if c >= 17:
                c = 0


class Cell:
    '''
    答えの任意の1文字
    '''
    def __init__(self, chara):
        self.char = chara
        self.is_checked = False
        self.state = CellState.INIT


class CellManager:
    '''
    答えのCellを5つ持つ

    TODO レベルを表すIntEnumを受け取り、応じた答えを作成する。
    不正な値であればデフォルトで作成する。
    '''
    def __init__(self, answer_name, pokemons):
        '''
        初期化

        Args:
            answer_name(string):  正解ポケモン名
            pokemons(list<string>):  回答可能なポケモン名
        '''
        self.kotae = answer_name
        self.answerable_names = pokemons
        self.answer_cells = {}
        for i, char in enumerate(list(self.kotae)):
            self.answer_cells[i] = Cell(char)

    def get_answer(self):
        return self.kotae

    def _reset_hit(self):
        for i in self.answer_cells.values():
            i.is_checked = False

    def hit(self, input_word):
        '''
        入力に対して答えと確認する。

        args:
            input_word:     回答文字列

        returns:
            "result":       実施結果
                                0:  正常終了
                                -1: 許可されない文字列
            "cells":        文字列に対する正誤
        '''
        if input_word not in self.answerable_names:
            return {"result": -1}
        self._reset_hit()
        input_cells = {}
        for i, c in enumerate(list(input_word)):
            input_cells[i] = Cell(c)

        # 場所と文字が一致しているか確認する
        for i, input_cell in input_cells.items():
            if i in self.answer_cells:
                if input_cell.char == self.answer_cells[i].char:
                    input_cell.state = CellState.GREEN
                    self.answer_cells[i].is_checked = True

        # 文字のみ一致しているものを確認する
        for input_cell in input_cells.values():
            if not input_cell.state == CellState.INIT:
                # 既に場所位置が一致している入力文字はスキップする
                continue
            for answer_cell in self.answer_cells.values():
                # 既に場所が特定された答え文字はスキップする
                if answer_cell.is_checked:
                    continue
                if input_cell.char == answer_cell.char:
                    input_cell.state = CellState.ORANGE
                    answer_cell.is_checked = True
                    break
                # 文字も外れていれば、ステート変化
                input_cell.state = CellState.MISS
        return {"result": 0, "cells":input_cells.values()}


class GameManager:
    def __init__(self, level_num):
        self._initialize(level_num)

    def _initialize(self, level_num):
        self.pokeManager = PokeNameManager()
        kotae = self.pokeManager.get_answer_pokemon(level_num)
        pokemons = self.pokeManager.get_answerable_pokemons(level_num)
        self.fifty_table = FiftyTable()
        self.cell_manager = CellManager(kotae, pokemons)

    def hit(self, string):
        return self.cell_manager.hit(string)

    def get_answer(self):
        return self.cell_manager.get_answer()

    # def regenerate(self, event=None):
    #     for item in self.labels:
    #         item.destroy()
    #     self.input.destroy()
    #     self.fifty_ui.destroy()

    #     self._initialize()
    #     self.main()
