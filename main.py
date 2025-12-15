def gcd(a, b):
    a = int(a)
    b = int(b)
    while b:
        a, b = b, a % b
    return abs(a)


def lcm(a, b):
    a = int(a)
    b = int(b)
    if a == 0 or b == 0:
        return 0
    return abs(a * b) // gcd(a, b)


def merge_counts(base, add, mult):
    for el in add:
        base[el] = base.get(el, 0) + add[el] * mult


def parse_formula(formula):
    formula = formula.strip()
    if not formula:
        return {}

    i = 0
    n = len(formula)
    lead_num = ""
    while i < n and formula[i].isdigit():
        lead_num += formula[i]
        i += 1
    leading_mult = int(lead_num) if lead_num else 1

    stack = [{}]
    bracket_stack = []

    pairs = {"(": ")", "[": "]", "{": "}"}

    while i < n:
        ch = formula[i]

        if ch in pairs:
            stack.append({})
            bracket_stack.append(ch)
            i += 1

        elif ch in pairs.values():
            if not bracket_stack:
                raise ValueError("Mismatched closing bracket in formula")
            open_br = bracket_stack.pop()
            expected = pairs[open_br]
            if ch != expected:
                raise ValueError("Mismatched brackets in formula")
            i += 1
            num = ""
            while i < n and formula[i].isdigit():
                num += formula[i]
                i += 1
            mult = int(num) if num else 1
            top = stack.pop()
            merge_counts(stack[-1], top, mult)

        elif ch.isalpha():
            element = formula[i]
            i += 1
            while i < n and formula[i].islower():
                element += formula[i]
                i += 1

            num = ""
            while i < n and formula[i].isdigit():
                num += formula[i]
                i += 1

            count = int(num) if num else 1
            stack[-1][element] = stack[-1].get(element, 0) + count

        else:
            i += 1

    if bracket_stack:
        raise ValueError("Unmatched opening bracket in formula")

    if leading_mult != 1:
        for k in stack[0]:
            stack[0][k] *= leading_mult

    return stack[0]


def parse_equation(eq):
    if "->" in eq:
        eq = eq.replace("->", "=")
    if "=>" in eq:
        eq = eq.replace("=>", "=")
    if "<-" in eq:
        eq = eq.replace("<-", "=")
    if "<->" in eq:
        eq = eq.replace("<->", "=")

    parts = eq.split("=")
    if len(parts) != 2:
        raise ValueError("Equation must contain a single '=' or arrow")

    left, right = parts[0], parts[1]
    left_compounds = [c.strip() for c in left.split("+") if c.strip()]
    right_compounds = [c.strip() for c in right.split("+") if c.strip()]

    compounds = left_compounds + right_compounds
    compound_data = [parse_formula(c) for c in compounds]

    elements = []
    for data in compound_data:
        for el in data:
            if el not in elements:
                elements.append(el)

    matrix = []
    for el in elements:
        row = []
        for i, comp in enumerate(compound_data):
            count = comp.get(el, 0)
            if i >= len(left_compounds):
                count = -count
            row.append(count)
        matrix.append(row)

    return matrix, compounds, len(left_compounds)


def solve_matrix(mat):
    class Frac:
        __slots__ = ("num", "den")

        def __init__(self, n, d=1):
            n = int(n)
            d = int(d)
            if d == 0:
                raise ZeroDivisionError("zero denominator")
            if n == 0:
                self.num = 0
                self.den = 1
            else:
                if d < 0:
                    n = -n
                    d = -d
                g = gcd(abs(n), d)
                self.num = n // g
                self.den = d // g

        def __add__(self, other):
            other = other if isinstance(other, Frac) else Frac(other)
            return Frac(
                self.num * other.den + other.num * self.den, self.den * other.den
            )

        def __sub__(self, other):
            other = other if isinstance(other, Frac) else Frac(other)
            return Frac(
                self.num * other.den - other.num * self.den, self.den * other.den
            )

        def __mul__(self, other):
            other = other if isinstance(other, Frac) else Frac(other)
            return Frac(self.num * other.num, self.den * other.den)

        def __truediv__(self, other):
            other = other if isinstance(other, Frac) else Frac(other)
            if other.num == 0:
                raise ZeroDivisionError
            return Frac(self.num * other.den, self.den * other.num)

        def __neg__(self):
            return Frac(-self.num, self.den)

        def is_zero(self):
            return self.num == 0

        def __repr__(self):
            return "%d/%d" % (self.num, self.den)

    rows = len(mat)
    if rows == 0:
        return []
    cols = len(mat[0])

    A = [[Frac(mat[i][j]) for j in range(cols)] for i in range(rows)]

    pivot_cols = []
    r = 0
    for c in range(cols):
        if r >= rows:
            break
        pivot = None
        for i in range(r, rows):
            if not A[i][c].is_zero():
                pivot = i
                break
        if pivot is None:
            continue
        A[r], A[pivot] = A[pivot], A[r]
        pv = A[r][c]
        inv = Frac(pv.den, pv.num)
        for j in range(c, cols):
            A[r][j] = A[r][j] * inv

        for i in range(rows):
            if i != r and not A[i][c].is_zero():
                factor = A[i][c]
                for j in range(c, cols):
                    A[i][j] = A[i][j] - factor * A[r][j]

        pivot_cols.append(c)
        r += 1

    free_cols = [c for c in range(cols) if c not in pivot_cols]
    if not free_cols:
        raise ValueError(
            "No non-trivial solution; equation cannot be balanced with given compounds"
        )

    sol = [Frac(0, 1) for _ in range(cols)]
    for fc in free_cols:
        sol[fc] = Frac(1, 1)

    for row_index in range(len(pivot_cols) - 1, -1, -1):
        c = pivot_cols[row_index]
        s = Frac(0, 1)
        for j in range(c + 1, cols):
            s = s + A[row_index][j] * sol[j]
        sol[c] = -s

    common_den = 1
    for f in sol:
        common_den = lcm(common_den, f.den)
    ints = [f.num * (common_den // f.den) for f in sol]

    g = 0
    for v in ints:
        g = gcd(g, v)
    if g == 0:
        g = 1
    ints = [v // g for v in ints]

    any_neg = any(v < 0 for v in ints)
    if any_neg:
        ints = [-v for v in ints]

    if all(v == 0 for v in ints):
        ints = [0] * (cols - 1) + [1]

    return ints


def format_equation(coeffs, compounds, split):
    left = []
    right = []

    for i, c in enumerate(coeffs):
        if c == 1:
            term = compounds[i]
        else:
            term = str(c) + compounds[i]
        if i < split:
            left.append(term)
        else:
            right.append(term)

    return " + ".join(left) + " = " + " + ".join(right)


def balance():
    try:
        eq = input("Equation (e.g. Ca(OH)2+HCl=CaCl2+H2O): ").strip()
        if not eq:
            print("No equation entered")
            return
        matrix, compounds, split = parse_equation(eq)
        coeffs = solve_matrix(matrix)
        print(format_equation(coeffs, compounds, split))
    except Exception as e:
        print("Error:", str(e))


if __name__ == "__main__":
    balance()
