# -*- coding: utf-8 -*-
from math import inf

def sell_in_change(item):
    if item.name == "Sulfuras, Hand of Ragnaros":
        return 0
    return -1

def quality_change(item):
    if item.name == "Sulfuras, Hand of Ragnaros":
        return 0
    if item.name == "Aged Brie":
        return 1
    if "Backstage passes" in item.name:
        if item.sell_in <= 5:
            return 3
        elif item.sell_in <= 10:
            return 2
        return 1

    # Everything else degrades in value:
    # * Items past sell-by degrade twice as fast
    # * Conjured items degrade twice as fast

    if item.sell_in < 0:
        sellby_multiplier = 2
    else:
        sellby_multiplier = 1
    if "Conjured" in item.name:
        conj_multiplier = 2
    else:
        conj_multiplier = 1
    return -1 * sellby_multiplier * conj_multiplier

def max_quality(item):
    if item.name == "Sulfuras, Hand of Ragnaros":
        return inf
    if "Backstage passes" in item.name and item.sell_in < 0:
        return 0
    return 50

def min_quality(item):
    if item.name == "Sulfuras, Hand of Ragnaros":
        return -inf
    return 0

class GildedRose(object):
    def __init__(self, items):
        self.items = items

    def update_quality(self):
        for item in self.items:
            item.sell_in += sell_in_change(item)
            new_quality = item.quality + quality_change(item)
            new_quality = max(min(new_quality, max_quality(item)), min_quality(item))
            item.quality = new_quality

class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
