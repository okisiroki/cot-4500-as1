# Assignment 1
# Jordan Sirokie 3831723

import math

def doubleFloatingToDecimal(input_number: str) -> float:
    s = input_number[0]
    exponent = input_number[1:12]
    mantissa = input_number[12:]

    c = 0
    # determine the numerical value from the exponent
    for index, bit in enumerate(exponent, start=-len(exponent)):
        c += int(bit) * 2**(-index-1)

    f = 0
    # determine the numerical value from the mantissa
    for index, bit in enumerate(mantissa):
        if int(bit) == 1:
            f = (1/2)**index

    # calculate the final value from the sign, exponent, and mantissa
    number = (-1)**int(s)*2**(c-1023)*(1+f)
    return number


def doubleChop(input_number: float, chop_length: int) -> float:
    if input_number < 1:
        magnitude = 0
        num = input_number
    else:
        # get magnitude of input number
        # (how many digits to the left of the decimal)
        magnitude = len(str(input_number).split(".")[0])
        # normalize input number
        num = input_number / (10**magnitude)
    # get first 5 digits
    num = int(str(num).split('.')[1][:chop_length])
    # return number to original magnitude
    num = num/10**(chop_length-magnitude)
    return num


def doubleRound(input_number: float, round_length: int) -> float:
    if str(input_number).split('.')[0] == "0":
        magnitude = 0
        num = input_number
    else:
        # get magnitude of input number
        magnitude = len(str(input_number).split(".")[0])
        # normalize input number
        num = input_number / (10**magnitude)
    # get first 6 digits (ignoring the 0.) and add 5
    num = int(str(num).split('.')[1][:round_length+1]) + 5
    num = int(str(num)[:round_length])
    # return number to original magnitude
    num = num/10**(round_length-magnitude)
    return num


def absolute_error(precise, approx) -> float:
    return abs(precise - approx)


def relative_error(precise, approx) -> float:
    return abs(precise - approx) / precise


def check_alt(function: str, x: int) -> bool:
    sample_size = 100 # must be even number
    i = 0
    # starting with 0, add 1 for a positive result and
    #   subtract -1 for a negative result. With an even 
    #   sample size and assuming the function is alternating, 
    #   the result should be 0.
    for k in range(1, sample_size + 1):
        y = eval(function)
        if y > 0:
            i += 1
        elif y < 0:
            i += -1
    if i == 0:
        return True
    else:
        return False


def check_decreasing(function: str, x: int) -> bool:
    sample_size = 100
    k = 1
    starting_val = abs(eval(function))
    # check for decreasing magnitude
    for k in range(2, sample_size + 1):
        result = abs(eval(function))
        if result >= starting_val: 
            return False
    return True


def minTerms(error: float) -> float:
    # (hardcoded based on the given series), not sure how to do otherwise
    # take the reciprocal to flip 1/(n+1)**3
    error = 1 / error
    # take the cube root to reduce (n+1)**3
    error = error ** (1/3)
    return math.ceil(error)


def minIterations(method: str, function: str, accuracy: float, a: int, b: int):
    if method.lower() == "bisection":
        # assumes inputs are on different sides of fucntion 
        diff = abs(b - a)
        i = 0
        while (diff >= accuracy):
            i += 1
            p = (a + b) / 2
            x = p

            midpoint = eval(function)
            if midpoint == 0.0:
                break
            
            x = a
            leftpoint = eval(function)

            # determine which function changed sign
            if (leftpoint<0 and midpoint>0) or (leftpoint>0 and midpoint<0):
                b = p
            else:
                a = p

            diff = abs(b - a)
        return i


    elif method.lower() == "newtonraphson":
        i = 0
        x = a

        function_derivative = "(3 * (x ** 2)) + (8 * x)"

        f = eval(function)
        f_prime = eval(function_derivative)
        approx = f / f_prime

        while (abs(approx) >= accuracy):
            i += 1

            f = eval(function)
            f_prime = eval(function_derivative)
            approx = f / f_prime

            x -= approx
        return i


if __name__ == "__main__":
    # Problem 1
    binary_number = "010000000111111010111001"
    decimal_number = doubleFloatingToDecimal(binary_number)
    print(f"{decimal_number}\n")

    # Problem 2
    chopped = doubleChop(decimal_number, 5)
    print(f"{chopped}\n")

    # Problem 3
    rounded = doubleRound(decimal_number, 5)
    print(f"{rounded}\n")

    # Problem 4
    print(f"{absolute_error(decimal_number, doubleRound(decimal_number, 3))}\n")
    print(f"{relative_error(decimal_number, doubleRound(decimal_number, 3))}\n")

    # Problem 5
    inf_series  = "((-1)**k) * ((x**k) / (k**3))"
    error = 10**-4
    x = 1

    check1 = check_alt(inf_series, x)
    check2 = check_decreasing(inf_series, x)
    if check1 and check2:
        min_terms = minTerms(error)
        print(f"{min_terms}\n")

    # Problem 6
    function = "(x**3) + (4 * (x**2)) - 10"
    acc = 10 ** (-4)
    a = 4
    b = 7
    print(f"{minIterations('Bisection', function, acc, a, b)}")
    print(f"{minIterations('NewtonRaphson', function, acc, a, b)}")
