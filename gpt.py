import random
from collections import defaultdict, Counter

NUM_GENERALS = 7
NUM_TRAITORS = 2
POSSIBLE_ORDERS = ['ATTACK', 'RETREAT']
SIMULATIONS = 100

def random_order():
    return random.choice(POSSIBLE_ORDERS)

# Global traitor set for simulation
traitors = set()

def is_traitor(general_id):
    return general_id in traitors

# Recursive message collector with path tracking
def OM_receive(m, path, receiver, order):
    sender = path[-1]
    if is_traitor(sender):
        order = random_order()

    if m == 0:
        return order

    sub_results = {
        receiver: order
    }
    for other in range(NUM_GENERALS):
        if other != receiver and other not in path:
            new_path = path + [receiver]
            if is_traitor(receiver):
                sub_results[other] = OM_receive(m - 1, new_path, other, order)
                sub_results[other] = random_order()

    # Majority vote among sub-results
    votes = list(sub_results.values())
    if votes:
        votes.append(order)
        majority = Counter(votes).most_common(1)[0][0]
        return majority
    else:
        return order

def run_simulation():
    global traitors
    generals = list(range(NUM_GENERALS))
    traitors = set(random.sample(generals, NUM_TRAITORS))

    commander = 0
    true_order = random_order()

    decisions = {}
    for lieutenant in generals:
        if lieutenant == commander:
            continue
        decision = OM_receive(m=2, path=[commander], receiver=lieutenant, order=true_order)
        decisions[lieutenant] = decision

    # Check if all loyal lieutenants agree
    loyal_decisions = {g: d for g, d in decisions.items() if g not in traitors}
    agreed = len(set(loyal_decisions.values())) == 1
    return agreed, decisions, traitors

# Run multiple simulations
success = 0
failures = 0
for _ in range(SIMULATIONS):
    agreed, decisions, traitors = run_simulation()
    if agreed:
        success += 1
    else:
        failures += 1
        loyal = {g: v for g, v in decisions.items() if g not in traitors}
        print(f"FAIL: Traitors={sorted(traitors)}, Loyal decisions={loyal}")

print(f"\nSimulated {SIMULATIONS} rounds with 2 traitors among 7 generals.")
print(f"Agreement among loyal lieutenants: {success} times")
print(f"Failures: {failures} times")
