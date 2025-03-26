import random
from typing import List, Dict, Any, Set
from collections import Counter

def majority(values: List[Any]) -> Any:
    """Return the majority value (breaking ties arbitrarily)."""
    majority = Counter(values).most_common(1)[0][0]
    return majority


def main():
    m = 2
    generals = [False for _ in range(m)] + [True for _ in range(2 * m + 1)]
    def om_algorithm(recipient, m, order, subset: Set[int]):
        if m == 0:
            if generals[recipient]:
                return order
            else:
                return random.choice([True, False])
        else:
            responses = []
            subset = {g for g in subset if g != recipient}
            if generals[recipient]:
                for gen_id in subset:
                    # print(f"General {recipient} is loyal, sending message to General {gen_id}")
                    responses.append(om_algorithm(gen_id, m - 1, order, subset))
                return majority([order] + responses)
            else:
                for gen_id in subset:
                    # print(f"General {recipient} is traitor, sending message to General {gen_id}")
                    responses.append(om_algorithm(gen_id, m - 1, random.choice([True, False]), subset))

                return random.choice([True, False])

    for sim_i in range(100):
        random.shuffle(generals)

        if generals[0]: # commander is loyal
            order = random.choice([True, False])
            subset = {i for i in range(1, len(generals))}
            decisions = [order] + [om_algorithm(i, m, order, subset) for i in range(1, len(generals))]
            for i, decision in enumerate(decisions):
                print(f"General {i} ({'loyal' if generals[i] else 'traitor'}) decision is {decision}")
        else: # commander is traitor
            order = [random.choice([True, False]) for _ in range(len(generals)-1)]
            subset = {i for i in range(1, len(generals))}
            decisions = [order] + [om_algorithm(i, m, order[i], subset) for i in range(0, len(generals)-1)]
            for i, decision in enumerate(decisions):
                print(f"General {i} ({'loyal' if generals[i] else 'traitor'}) decision is {decision}")

        loyal_decisions = [decision for i, decision in enumerate(decisions) if generals[i]]
        agreement = len(set(loyal_decisions)) == 1
        print("Agreement:", agreement)
        print()

        if not agreement:
            break






if __name__ == "__main__":
    main()
        