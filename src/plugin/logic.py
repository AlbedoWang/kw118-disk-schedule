from itertools import pairwise

from contract import ComputeOutput


def compute(v, workspace):
    if v.cylinders < 1 or any(not 0 <= x < v.cylinders for x in [v.head] + v.requests):
        raise ValueError("cylinder out of range")
    remaining = list(range(len(v.requests)))
    order, path = [], [v.head]
    if v.policy.value == "scan":
        same = [i for i in remaining if v.requests[i] == v.head]
        up = sorted((i for i in remaining if v.requests[i] > v.head), key=lambda i: (v.requests[i], i))
        down = sorted((i for i in remaining if v.requests[i] < v.head), key=lambda i: (-v.requests[i], i))
        first, second = (up, down) if v.direction.value == "up" else (down, up)
        for i in same + first:
            order.append(i)
            path.append(v.requests[i])
        if second:
            path.append(v.cylinders - 1 if v.direction.value == "up" else 0)
        for i in second:
            order.append(i)
            path.append(v.requests[i])
    else:
        while remaining:
            i = (
                remaining[0]
                if v.policy.value == "fcfs"
                else min(remaining, key=lambda i: (abs(v.requests[i] - path[-1]), v.requests[i], i))
            )
            remaining.remove(i)
            order.append(i)
            path.append(v.requests[i])
    return ComputeOutput(order, path, sum(abs(a - b) for a, b in pairwise(path)))
