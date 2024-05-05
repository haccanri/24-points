import itertools
import operator
import queue
from typing import List, Callable, Any, Tuple

import numpy as np

OPS = [operator.add, operator.sub, operator.mul, operator.truediv]

def get_valid_ops(n1: int, n2: int) -> List[List[Any]]:
    """
    Return the valid ops list for n1 and n2.

    if op == operator.sub,
        only max(n1, n2) - min(n1, n2) is valid
    if op == operator.truediv,
        only when max(n1, n2) // min(n1, n2) == 0,
        max(n1, n2) / min(n1, n2) is valid

    Return
    """
    if n1 < n2:
        large = n2
        small = n1
    else:
        large = n1
        small = n2

    res = [
        [large, small, operator.add],
        [large, small, operator.sub],
        [large, small, operator.mul]
    ]

    if small > 0.01 and large % small == 0:
        res.append([large, small, operator.truediv])
    return res

def get_remain_list(arr: List[Any], id1: int, id2: int) -> List[Any]:
    '''Return a new array without elements at id1 and id2.'''
    return [arr[i] for i in range(len(arr)) if i != id1 and i != id2]

def reduce(nums: List[int], op_list: List[List[Any]] = []) -> Tuple[List[int], List[List[Any]]]:
    # 随机选择两个数进行运算，将数组变成长度减少1的数组
    # input: nums. original array
    # output: (array_list, op_list)
    assert len(nums) > 1
    pairs_index = itertools.combinations(range(0, len(nums)), 2)
    arr = []
    ops = []
    for id1, id2 in pairs_index:
        remain = get_remain_list(nums, id1, id2)
        for large, small, op in get_valid_ops(nums[id1], nums[id2]):
            reduced_list = remain.copy()
            reduced_list.append(op(large, small))
            op_history = op_list.copy()
            op_history.append([large, small, op])
            arr.append(reduced_list)
            ops.append(op_history)

    return arr, ops

def to_tuple(sol):
    return tuple(tuple(t) for t in sol)

def to_list(sol):
    return [list(s) for s in sol]

def search(nums, target=24, deduplicate=True):
    q = queue.Queue()
    q.put((nums.copy(), []))
    count = 0
    solutions = []

    while not q.empty():
        res, ops = q.get()
        res, ops = reduce(res, op_list=ops)
        for r, o in zip(res, ops):
            if len(r) == 1:
                count += 1
                if r[0] == target:
                    solutions.append(o)
            else:
                q.put((r, o))

    print(f'searched {count} formulars')
    if deduplicate:
        dedup_set = set(to_tuple(s) for s in solutions)
        solutions = [to_list(s) for s in dedup_set]
    print(f'found {len(solutions)} solutions')
    return solutions

def show(solution, nums=None):
    print('=' * 24)
    if nums is not None:
        arr = nums.copy()
        print(' '.join(str(n) for n in nums))
    for n1, n2, op in solution:
        print(f'{n1} {op.__name__} {n2} = {op(n1, n2)}')
        if nums is not None:
            arr.remove(n1)
            arr.remove(n2)
            arr.append(op(n1, n2))
            print(' '.join(str(n) for n in arr))
    print('=' * 24)

def solve(nums):
    sols = search(nums)
    for s in sols:
        show(s, nums)

if __name__ == '__main__':
    '''
    print(get_valid_ops(3, 4))
    print(get_valid_ops(4, 3))
    print(get_valid_ops(3, 6))

    print('get_remain_list([1, 2], 0, 1):', get_remain_list([1, 2], 0, 1))

    arr, ops = (reduce([3, 4, 5]))
    print(arr)
    print(ops)

    arr, ops = (reduce([3, 4, 6]))
    print(arr)
    print(ops)
    '''
    nums = [5, 6, 7, 8]
    solutions = search(nums)
    for s in solutions:
        show(s, nums)