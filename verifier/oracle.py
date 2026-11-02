from contract import ComputeOutput


def input_problem(v):
    if v.cylinders <= 0 or not 0 <= v.head < v.cylinders or any(x < 0 or x >= v.cylinders for x in v.requests):
        return "invalid cylinder"
    return None


def expected(v):
    pending = set(range(len(v.requests)))
    path, order = [v.head], []
    direction = 1 if v.direction.value == "up" else -1
    while pending:
        if v.policy.value == "fcfs":
            chosen = min(pending)
        elif v.policy.value == "sstf":
            chosen = min(pending, key=lambda i: (abs(path[-1] - v.requests[i]), v.requests[i], i))
        else:
            candidates = [i for i in pending if (v.requests[i] - path[-1]) * direction >= 0]
            if not candidates:
                path.append(v.cylinders - 1 if direction == 1 else 0)
                direction = -direction
                continue
            chosen = min(candidates, key=lambda i: (abs(v.requests[i] - path[-1]), i))
        order.append(chosen)
        path.append(v.requests[chosen])
        pending.remove(chosen)
    return ComputeOutput(order, path, sum(abs(path[i] - path[i - 1]) for i in range(1, len(path))))
