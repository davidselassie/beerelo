#!/usr/bin/env python3
from collections import namedtuple
from collections import defaultdict
from operator import itemgetter


Match = namedtuple('Match', ('winner', 'loser'))

matches = (
    Match("Olympia", "Rainier"),
    Match("Olympia", "Milwaukee's Best Ice"),
    Match("Olympia", "Budweiser"),
    Match("PBR", "Rainier"),
    Match("PBR", "High Life"),
    Match("PBR", "High Life"),
    Match("PBR", "Milwaukee's Best Ice"),
    Match("Rainier", "High Life"),
    Match("High Life", "Rainier"),
    Match("High Life", "Rainier"),
    Match("High Life", "Budweiser"),
    Match("Milwaukee's Best Ice", "Olympia"),
    Match("Milwaukee's Best Ice", "Olympia"),
    Match("Milwaukee's Best Ice", "Rolling Rock"),
    Match("Milwaukee's Best Ice", "PBR"),
    Match("Budweiser", "Olympia"),
    Match("Budweiser", "Rolling Rock"),
    Match("Budweiser", "High Life"),
    Match("Hamm's", "Rolling Rock"),
    Match("Hamm's", "PBR"),
    Match("Hamm's", "Rainier"),
    Match("Hamm's", "Budweiser"),
    Match("Hamm's", "Budweiser"),
    Match("Rolling Rock", "Olympia"),
    Match("Rolling Rock", "Olympia"),
)

def start_rating():
    return 1600.0

name_to_rating = defaultdict(start_rating)
counts = defaultdict(int)

def expected_rating(rating_a, rating_b):
    return 1 / (1 + 10 ** ((rating_b - rating_a) / 400))

def match_updated_ratings(winner_rating, loser_rating, k):
    return (
        winner_rating + k * (1 - expected_rating(
            winner_rating,
            loser_rating
        )),
        loser_rating + k * (0 - expected_rating(
            loser_rating,
            winner_rating
        )),
    )

def print_stat(name_to_stat, stat_name):
    col_width = max(len(name) for name in name_to_stat.keys())
    def fmt_str(fill):
        return '{{0:{0}>{1}}}|{{1:{0}<10}}'.format(fill, col_width)

    print(fmt_str(' ').format('Beer', stat_name))
    print(fmt_str('-').format('-', '-'))
    for name_stat in sorted(
            name_to_stat.items(),
            key=itemgetter(1),
            reverse=True):
        name, stat = name_stat
        print(fmt_str(' ').format(name, round(stat)))

for match in matches:
    (
        name_to_rating[match.winner],
        name_to_rating[match.loser],
    ) = match_updated_ratings(
        name_to_rating[match.winner],
        name_to_rating[match.loser],
        40
    )
    counts[match.winner] += 1
    counts[match.loser] += 1

print_stat(name_to_rating, 'Elo Rating')
print()
print_stat(counts, 'Counts')
