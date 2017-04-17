from math import sqrt

critics = {'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
                         'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5,
                         'The Night Listener': 3.0},
           'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5,
                            'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0,
                            'You, Me and Dupree': 3.5},
           'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
                                'Superman Returns': 3.5, 'The Night Listener': 4.0},
           'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
                            'The Night Listener': 4.5, 'Superman Returns': 4.0,
                            'You, Me and Dupree': 2.5},
           'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
                            'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0,
                            'You, Me and Dupree': 2.0},
           'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
                             'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
           'Toby': {'Snakes on a Plane': 4.5, 'You, Me and Dupree': 1.0, 'Superman Returns': 4.0}}


# Returns a distance-based similarity score for person1 and person2
def sim_distance(preferences, person1, person2):
    # Get the list of shared_items
    si = {}
    for item in preferences[person1]:
        if item in preferences[person2]:
            si[item] = 1
    # if they have no ratings in common, return 0
    if len(si) == 0: return 0
    # Add up the squares of all the differences
    sum_of_squares = sum([pow(preferences[person1][item] - preferences[person2][item], 2)
                          for item in preferences[person1] if item in preferences[person2]])
    return 1 / (1 + sum_of_squares)


def sim_pearson(preferences, person1, person2):
    si = {}

    for item in preferences[person1]:
        if item in preferences[person2]:
            si[item] = 1
    n = len(si)

    if n == 0:
        return 0

    sum1 = sum([preferences[person1][it] for it in si])
    sum2 = sum([preferences[person2][it] for it in si])

    sum1Sq = sum([pow(preferences[person1][it], 2) for it in si])
    sum2Sq = sum([pow(preferences[person2][it], 2) for it in si])

    pSum = sum([preferences[person1][it] * preferences[person2][it] for it in si])

    num = pSum - (sum1 * sum2 / n)

    den = sqrt((sum1Sq - pow(sum1, 2) / n) * (sum2Sq - pow(sum2, 2) / n))

    if den == 0:
        return 0

    r = num / den

    return r


