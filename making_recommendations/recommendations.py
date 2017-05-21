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
    if len(si) == 0:
        return 0
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

    sum1_sq = sum([pow(preferences[person1][it], 2) for it in si])
    sum2_sq = sum([pow(preferences[person2][it], 2) for it in si])

    p_sum = sum([preferences[person1][it] * preferences[person2][it]
                 for it in si])

    num = p_sum - (sum1 * sum2 / n)

    den = sqrt((sum1_sq - pow(sum1, 2) / n) * (sum2_sq - pow(sum2, 2) / n))

    if den == 0:
        return 0

    r = num / den

    return r


def top_matches(preferences, person, n=5, similarity=sim_pearson):
    scores = [(similarity(preferences, person, other), other)
              for other in preferences if other != person
              ]

    scores.sort()
    scores.reverse()
    return scores[0:n]


def get_recommendations(preferences, person, similarity=sim_pearson):
    totals = {}
    sim_sums = {}
    for other in preferences:
        if other == person:
            continue
        sim = similarity(preferences, person, other)

        if sim <= 0:
            continue

        for item in preferences[other]:
            if item not in preferences[person] or preferences[person][item] == 0:
                totals.setdefault(item, 0)
                totals[item] += preferences[other][item] * sim
                sim_sums.setdefault(item, 0)
                sim_sums[item] += sim

    rankings = [(total / sim_sums[item], item)
                for item, total in totals.items()]

    rankings.sort()
    rankings.reverse()

    return rankings


def transform_preferences(preferences):
    result = {}
    for person in preferences:
        for item in preferences[person]:
            result.setdefault(item, {})

            result[item][person] = preferences[person][item]

    return result


def calculate_similar_items(preferences, n=10):
    result = {}

    item_preferences = transform_preferences(preferences)
    c = 0
    for item in item_preferences:
        c += 1
        if c % 100 == 0: print "%d / %d" % (c, len(item_preferences))
        scores = top_matches(item_preferences, item, n=n, similarity=sim_pearson)
        result[item] = scores
    return result


def get_recommended_items(preferences, item_match, user):
    user_ratings = preferences[user]
    scores = {}
    total_sim = {}

    for (item, rating) in user_ratings.items():
        for (similarity, item2) in item_match[item]:
            if item2 in user_ratings: continue

            scores.setdefault(item2, 0)
            scores[item2] += similarity * rating

            total_sim.setdefault(item2, 0)
            total_sim[item2] += similarity

    rankings = [(score / total_sim[item], item) for item, score in scores.items()]

    rankings.sort()
    rankings.reverse()
    return rankings
