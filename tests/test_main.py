import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import main


def test_parse_formula_simple():
    assert main.parse_formula("H2O") == {"H": 2, "O": 1}


def test_parse_formula_parentheses():
    assert main.parse_formula("Ca(OH)2") == {"Ca": 1, "O": 2, "H": 2}


def test_parse_formula_brackets():
    got = main.parse_formula("K4[ON(SO3)2]2")
    assert got.get("K") == 4
    assert got.get("O") == 14
    assert got.get("N") == 2
    assert got.get("S") == 4


def test_leading_multiplier():
    assert main.parse_formula("2H2O") == {"H": 4, "O": 2}


def test_balance_simple():
    m, comps, split = main.parse_equation("H2+O2=H2O")
    coeffs = main.solve_matrix(m)
    assert coeffs == [2, 1, 2]
    out = main.format_equation(coeffs, comps, split)
    assert out == "2H2 + O2 = 2H2O"


def test_balance_combustion():
    m, comps, split = main.parse_equation("C3H8+O2=CO2+H2O")
    coeffs = main.solve_matrix(m)
    assert coeffs == [1, 5, 3, 4]


def test_no_solution_raises():
    with pytest.raises(ValueError):
        m, comps, split = main.parse_equation("K4[ON(SO3)2]2=K2S2O8+N2O")
        main.solve_matrix(m)
        main.solve_matrix(m)
        main.solve_matrix(m)
        main.solve_matrix(m)
