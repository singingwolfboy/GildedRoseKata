# -*- coding: utf-8 -*-
import unittest

from gilded_rose import Item, GildedRose

class GildedRoseTest(unittest.TestCase):
    def test_consistent_items(self):
        item = Item("foo", 0, 0)
        items = [item]
        gilded_rose = GildedRose(items)
        self.assertEqual(gilded_rose.items, items)
        gilded_rose.update_quality()
        self.assertEqual(gilded_rose.items, items)
        self.assertEqual(item.name, "foo")

class GildedRoseUpdateQualityTest(unittest.TestCase):
    def setUp(self):
        self.dexvest = Item(name="+5 Dexterity Vest", sell_in=10, quality=20)
        self.brie = Item(name="Aged Brie", sell_in=2, quality=0)
        self.elixir = Item(name="Elixir of the Mongoose", sell_in=5, quality=7)
        self.sulfuras = Item(name="Sulfuras, Hand of Ragnaros", sell_in=1, quality=80)
        self.backstage = Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=15, quality=20)
        self.conjured = Item(name="Conjured Mana Cake", sell_in=2, quality=10)
        self.bread = Item(name="Bread", sell_in=1, quality=10)
        self.moldy = Item(name="Moldy Bread", sell_in=-1, quality=0)

        self.shop = GildedRose([
            self.dexvest, self.brie, self.elixir, self.sulfuras,
            self.backstage, self.conjured, self.bread, self.moldy,
        ])

    def test_sell_in_drops(self):
        self.assertEqual(self.dexvest.sell_in, 10)
        self.shop.update_quality()
        self.assertEqual(self.dexvest.sell_in, 9)
        self.shop.update_quality()
        self.assertEqual(self.dexvest.sell_in, 8)

    def test_sell_in_drops_negative(self):
        self.assertEqual(self.moldy.sell_in, -1)
        self.shop.update_quality()
        self.assertEqual(self.moldy.sell_in, -2)
        self.shop.update_quality()
        self.assertEqual(self.moldy.sell_in, -3)

    def test_quality_drops(self):
        self.assertEqual(self.dexvest.quality, 20)
        self.shop.update_quality()
        self.assertEqual(self.dexvest.quality, 19)
        self.shop.update_quality()
        self.assertEqual(self.dexvest.quality, 18)

    def test_quality_drops_faster_when_past_sell_in(self):
        self.assertEqual(self.bread.quality, 10)
        self.assertEqual(self.bread.sell_in, 1)
        self.shop.update_quality()
        self.assertEqual(self.bread.quality, 9)
        self.assertEqual(self.bread.sell_in, 0)
        # drops faster now that sell_in is zero
        self.shop.update_quality()
        self.assertEqual(self.bread.quality, 7)
        self.assertEqual(self.bread.sell_in, -1)
        self.shop.update_quality()
        self.assertEqual(self.bread.quality, 5)
        self.assertEqual(self.bread.sell_in, -2)

    def test_quality_min_zero(self):
        self.assertEqual(self.dexvest.quality, 20)
        for _ in range(100):
            self.shop.update_quality()
        self.assertEqual(self.dexvest.quality, 0)

    def test_quality_brie(self):
        self.assertEqual(self.brie.quality, 0)
        self.shop.update_quality()
        self.assertEqual(self.brie.quality, 1)
        self.shop.update_quality()
        self.assertEqual(self.brie.quality, 2)

    def test_quality_brie_max_fifty(self):
        for _ in range(100):
            self.shop.update_quality()
        self.assertEqual(self.brie.quality, 50)

    def test_backstage(self):
        self.assertEqual(self.backstage.sell_in, 15)
        self.assertEqual(self.backstage.quality, 20)
        self.shop.update_quality()
        self.assertEqual(self.backstage.sell_in, 14)
        self.assertEqual(self.backstage.quality, 21)
        self.shop.update_quality()
        self.assertEqual(self.backstage.sell_in, 13)
        self.assertEqual(self.backstage.quality, 22)

    def test_backstage_ten_days_left(self):
        self.backstage.sell_in = 10
        self.assertEqual(self.backstage.quality, 20)
        self.shop.update_quality()
        self.assertEqual(self.backstage.sell_in, 9)
        self.assertEqual(self.backstage.quality, 22)
        self.shop.update_quality()
        self.assertEqual(self.backstage.sell_in, 8)
        self.assertEqual(self.backstage.quality, 24)

    def test_backstage_five_days_left(self):
        self.backstage.sell_in = 5
        self.assertEqual(self.backstage.quality, 20)
        self.shop.update_quality()
        self.assertEqual(self.backstage.quality, 23)
        self.assertEqual(self.backstage.sell_in, 4)
        self.shop.update_quality()
        self.assertEqual(self.backstage.quality, 26)
        self.assertEqual(self.backstage.sell_in, 3)

    def test_backstage_expires(self):
        self.backstage.sell_in = 5
        self.assertEqual(self.backstage.quality, 20)
        for _ in range(5):
            self.shop.update_quality()
        self.assertEqual(self.backstage.quality, 35)
        self.assertEqual(self.backstage.sell_in, 0)
        # expired!
        self.shop.update_quality()
        self.assertEqual(self.backstage.quality, 0)
        self.assertEqual(self.backstage.sell_in, -1)
        self.shop.update_quality()
        self.assertEqual(self.backstage.quality, 0)
        self.assertEqual(self.backstage.sell_in, -2)

    def test_backstage_max_quality(self):
        self.backstage.quality = 45
        self.backstage.sell_in = 10
        self.shop.update_quality()
        self.assertEqual(self.backstage.quality, 47)
        self.assertEqual(self.backstage.sell_in, 9)
        self.shop.update_quality()
        self.assertEqual(self.backstage.quality, 49)
        self.assertEqual(self.backstage.sell_in, 8)
        self.shop.update_quality()
        # max quality is 50
        self.assertEqual(self.backstage.quality, 50)
        self.assertEqual(self.backstage.sell_in, 7)
        self.shop.update_quality()
        self.assertEqual(self.backstage.quality, 50)
        self.assertEqual(self.backstage.sell_in, 6)

    def test_sulfuras_constant(self):
        self.assertEqual(self.sulfuras.sell_in, 1)
        self.assertEqual(self.sulfuras.quality, 80)
        self.shop.update_quality()
        self.assertEqual(self.sulfuras.sell_in, 1)
        self.assertEqual(self.sulfuras.quality, 80)

    def test_quality_conjured(self):
        self.assertEqual(self.conjured.quality, 10)
        self.assertEqual(self.conjured.sell_in, 2)
        self.shop.update_quality()
        self.assertEqual(self.conjured.quality, 8)
        self.assertEqual(self.conjured.sell_in, 1)
        self.shop.update_quality()
        self.assertEqual(self.conjured.quality, 6)
        self.assertEqual(self.conjured.sell_in, 0)
        # drops faster now that sell_in is zero
        self.shop.update_quality()
        self.assertEqual(self.conjured.quality, 2)
        self.assertEqual(self.conjured.sell_in, -1)
        self.shop.update_quality()
        self.assertEqual(self.conjured.quality, 0)
        self.assertEqual(self.conjured.sell_in, -2)
        self.shop.update_quality()
        self.assertEqual(self.conjured.quality, 0)
        self.assertEqual(self.conjured.sell_in, -3)


if __name__ == '__main__':
    unittest.main()
