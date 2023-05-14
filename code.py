import numpy

# constants
stepcost = -0.04
pdir = 0.7
pperp = 0.15
gamma = 0.95
limit = 0.0001

m = 4
n = 3
util = [[0.0 for j in range(n)] for i in range(m)]
# print(util)

util[0][1] = 1.0
util[0][2] = -1.0
util[2][1] = 2.0
prev_util = numpy.copy(util)
# print("util: \n", util)
# print("prev: \n", prev_util)

dir = [["" for j in range(n)] for i in range(m)]

noi = 0
while True:
    flag = 0
    noi = noi + 1
    print("Iteration", noi, "utility values:")

    for i in range(m):
        for j in range(n):
            # nothing to do if wall or reward or penalty state
            if util[i][j] == 2.0 or util[i][j] == 1.0 or util[i][j] == -1.0:
                dir[i][j] = "N/A"
                continue

            # up
            upval = 0
            if ((i - 1) < 0) or (util[i - 1][j] == 2.0):
                upval = prev_util[i][j]
            else:
                upval = prev_util[i - 1][j]

            #
            downval = 0
            if ((i + 1) >= m) or (util[i + 1][j] == 2.0):
                downval = prev_util[i][j]
            else:
                downval = prev_util[i + 1][j]

            # left
            leftval = 0
            if ((j - 1) < 0) or (util[i][j - 1] == 2.0):
                leftval = prev_util[i][j]
            else:
                leftval = prev_util[i][j - 1]

            # right
            rightval = 0
            if ((j + 1) >= n) or (util[i][j + 1] == 2.0):
                rightval = prev_util[i][j]
            else:
                rightval = prev_util[i][j + 1]

            upsum = upval * pdir + leftval * pperp + rightval * pperp
            downsum = downval * pdir + leftval * pperp + rightval * pperp
            leftsum = leftval * pdir + upval * pperp + downval * pperp
            rightsum = rightval * pdir + upval * pperp + downval * pperp

            # if i == 1 and j == 1:
            #     print(upsum, downsum, leftsum, rightsum)
            maxsum = max(upsum, downsum, leftsum, rightsum)
            if maxsum == upsum:
                dir[i][j] = "up"
            elif maxsum == downsum:
                dir[i][j] = "down"
            elif maxsum == rightsum:
                dir[i][j] = "right"
            else:
                dir[i][j] = "left"

            maxutil = stepcost + gamma * maxsum
            util[i][j] = maxutil

            if flag == 0:
                if abs(prev_util[i][j] - util[i][j]) > limit:
                    flag = 1

    print(numpy.array(util))
    print()

    if flag == 0:
        break
    prev_util = numpy.copy(util)

print("Convergence happens in", noi, "iterations")
# print(util)
print("----------------------------------------")
print()
print("Bonus")
print()
print("Policy of each cell after convergence:")
print(numpy.array(dir))
