#!/usr/bin/env python3
"""Validate software-estimator JSON data."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


REQUIRED_TOP_LEVEL_KEYS = {
    "project",
    "pricing",
    "summary",
    "functions",
    "implementation_details",
    "risks",
    "confirmation_questions",
}

FUNCTION_REQUIRED_KEYS = {
    "module",
    "function",
    "included_terminals",
    "base_total_days",
    "buff_percent",
    "buff_days",
    "final_total_days",
    "quotation_amount",
}

ALLOWED_TERMINALS = {
    "iOS",
    "Android",
    "管理后台Web",
    "H5",
    "小程序",
    "PC Web",
    "服务端",
    "开放API",
}


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as file_obj:
        data = json.load(file_obj)
    if not isinstance(data, dict):
        raise ValueError("JSON root must be an object")
    return data


def _require_keys(container: dict[str, Any], keys: set[str], label: str, errors: list[str]) -> None:
    missing = sorted(keys - set(container))
    if missing:
        errors.append(f"{label} missing required keys: {', '.join(missing)}")


def _is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def validate_estimate(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    _require_keys(data, REQUIRED_TOP_LEVEL_KEYS, "root", errors)
    if errors:
        return errors

    functions = data.get("functions")
    if not isinstance(functions, list) or not functions:
        errors.append("functions must be a non-empty list")
        return errors

    pricing = data.get("pricing", {})
    if not isinstance(pricing, dict):
        errors.append("pricing must be an object")
    else:
        pricing_mode = pricing.get("pricing_mode")
        person_day_price = pricing.get("person_day_price")
        role_prices = pricing.get("role_prices", {})
        if pricing_mode == "unified":
            if not _is_number(person_day_price) or person_day_price <= 0:
                errors.append("pricing.person_day_price must be a positive number in unified pricing mode")
        elif pricing_mode == "role_based":
            if not isinstance(role_prices, dict) or not role_prices:
                errors.append("pricing.role_prices must be a non-empty object in role_based pricing mode")
            else:
                invalid_roles = [
                    role for role, price in role_prices.items()
                    if not isinstance(role, str) or not _is_number(price) or price <= 0
                ]
                if invalid_roles:
                    errors.append("pricing.role_prices contains invalid role prices")
        else:
            errors.append("pricing.pricing_mode must be unified or role_based")

        coefficient = pricing.get("quotation_coefficient")
        if not _is_number(coefficient) or coefficient <= 0:
            errors.append("pricing.quotation_coefficient must be a positive number confirmed by the user")

    project_terminals = data.get("project", {}).get("included_terminals", [])
    if not isinstance(project_terminals, list):
        errors.append("project.included_terminals must be a list")
    else:
        invalid = sorted(set(project_terminals) - ALLOWED_TERMINALS)
        if invalid:
            errors.append(f"project.included_terminals contains invalid terminals: {', '.join(invalid)}")

    project_level_buff = bool(data.get("summary", {}).get("project_level_buff_applied", False))
    has_function_buff = False

    numeric_keys = {
        "base_total_days",
        "buff_percent",
        "buff_days",
        "final_total_days",
        "quotation_amount",
    }

    for index, item in enumerate(functions, start=1):
        if not isinstance(item, dict):
            errors.append(f"functions[{index}] must be an object")
            continue
        _require_keys(item, FUNCTION_REQUIRED_KEYS, f"functions[{index}]", errors)

        terminals = item.get("included_terminals", [])
        if not isinstance(terminals, list) or not terminals:
            errors.append(f"functions[{index}].included_terminals must be a non-empty list")
        else:
            invalid = sorted(set(terminals) - ALLOWED_TERMINALS)
            if invalid:
                errors.append(f"functions[{index}] has invalid terminals: {', '.join(invalid)}")

        for key in numeric_keys:
            value = item.get(key)
            if key in item and not _is_number(value):
                errors.append(f"functions[{index}].{key} must be numeric")

        if _is_number(item.get("buff_days")) and item["buff_days"] > 0:
            has_function_buff = True

        base = item.get("base_total_days")
        buff = item.get("buff_days")
        final = item.get("final_total_days")
        if _is_number(base) and _is_number(buff) and _is_number(final):
            if abs((base + buff) - final) > 0.05:
                errors.append(
                    f"functions[{index}] final_total_days must equal base_total_days + buff_days"
                )

    if project_level_buff and has_function_buff:
        errors.append("Buff double-counting: project-level Buff and function-level Buff both applied")

    return errors


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("Usage: validate_estimate_data.py <estimate.json>", file=sys.stderr)
        return 1

    try:
        data = load_json(Path(argv[1]))
        errors = validate_estimate(data)
    except Exception as exc:
        print(f"Validation failed: {exc}", file=sys.stderr)
        return 1

    if errors:
        print("Validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("Validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
