# Chemical Equation Balancer for Casio fx-CG50

A small MicroPython-compatible program to balance chemical equations using
integer-only arithmetic and exact rational elimination. Designed to run on
Casio fx-CG50 (MicroPython) and also testable on a desktop Python environment.

## Features

- Supports nested parentheses and brackets: (), [], {}
- Integer-only math (no floats) suitable for MicroPython on calculators
- Exact rational elimination to find minimal integer coefficients
- Simple, dependency-free single-file `main.py`

## Highlights

- Parentheses parsing: supports nested groups using (), [], and {} with trailing multipliers (e.g., K4[ON(SO3)2]2) and leading multipliers (e.g., 2H2O). The parser is permissive but validates bracket matching to avoid malformed input.
- Integer-only Gaussian elimination: the solver uses exact rational arithmetic implemented with integer numerators and denominators (no floating point). It computes a null-space vector, clears denominators, and reduces by the greatest common divisor to return the smallest whole-number coefficient ratio.
- MicroPython constraints: designed for limited-memory devices like the Casio fx-CG50. The code avoids external libraries, floating point math, heavy recursion, and large temporary allocations; error messages are kept simple for small consoles.

## Usage (Casio fx-CG50)

1. Copy `main.py` to your calculator's file system (root or preferred folder).
2. Run `main.py` and enter an equation like:

```
Ca(OH)2+HCl=CaCl2+H2O
```

3. The program prints the balanced equation or an error message if it can't
   find a non-trivial balance.

## Usage (local testing)

1. Create a virtual environment and activate it (optional but recommended):

```bash
python -m venv .venv
source .venv/bin/activate  # or .\.venv\Scripts\activate on Windows
```

2. Install pytest and run tests:

```bash
pip install pytest
pytest -q
```

## Project notes

- This project avoids recursion and floating point arithmetic for compatibility
  with MicroPython on constrained devices.
- If an equation cannot be balanced (only the trivial all-zero solution), the
  program raises a clear error.

## License

This project is licensed under the [MIT License](LICENSE).
