def create_defense_map():
    return [[0.0 for _ in range(28)] for _ in range(14)]


def flip_coords(x, y):
    return x, 13 - y


def update_defense_map(map, damages=None, breaches=None, alpha=0.5, eta=0.5):
    """
    damages : [[x1, y1, dmg1], [x2, y2, dmg2], ..., [xn, yn, dmgn]]
    breaches : [[x1, y1, score1], [x2, y2, score2], ..., [xn, yn, scoren]]
    severity = alpha*dmg + (1 - alpha)*score
    """

    if damages is not None:
        for (x_real, y_real, dmg) in damages:
            x_map, y_map = flip_coords(x_real, y_real)
            map[x_map][y_map] += alpha*dmg

    if breaches is not None:
        for (x_real, y_real, score) in breaches:
            x_map, y_map = flip_coords(x_real, y_real)
            map[x_map][y_map] += (1. - alpha)*score

    sum = 0.0
    for i in range(14):
        for j in range(28):
            map[i][j] *= eta
            sum += map[i][j]

    return map, sum


if __name__ == '__main__':
    defense_map = create_defense_map()
    map, score = update_defense_map(defense_map, damages=[[11, 6, 2], [1, 12, 6]])
    assert(defense_map[11][7] == 0.5)
    assert(defense_map[1][1] == 1.5)
    assert(score == 2)
