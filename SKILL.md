---
name: software-estimator
description: Estimate software development effort and customer quotation from requirements in documents, spreadsheets, images, or chat. Use when Codex needs to read software requirements, identify terminals such as iOS, Android, Web admin, H5, mini program, or PC Web, ask estimation prerequisites, judge standard-product coverage, calculate role and terminal person-days, add Buff time with reasons, and generate a Chinese Excel workbook with function quotation, implementation details, risks, assumptions, and customer confirmation questions.
---

# Software Estimator

## Overview

Use this skill to convert software requirements into a structured effort and quotation workbook. Always keep base effort, risk adjustment, and Buff time traceable.

## Workflow

1. Read the requirement source. For spreadsheets use the spreadsheets skill when available; for PDFs use the PDF skill when needed; for images extract visible text and note uncertainty.
2. Identify the likely business domain and load only the relevant file from `references/knowledge/`. Always load `references/knowledge/common-modules.md`.
3. Load `references/output-schema.md`, `references/estimation-baseline.md`, `references/coverage-rules.md`, `references/risk-rules.md`, and `references/buff-rules.md`.
4. Ask required pre-estimation questions before generating the final workbook. If the user cannot answer, continue with explicit assumptions and add them to the customer confirmation questions.
5. Split the scope into first-level modules and customer-readable second-level functions.
6. Split each function into internal implementation items by terminal and role.
7. Estimate base person-days by role and terminal.
8. Apply coverage, complexity, and risk coefficients.
9. Add Buff percentage, Buff person-days, and Buff reason separately from base effort.
10. Create structured estimate JSON matching `references/output-schema.md`.
11. Run `scripts/validate_estimate_data.py` on the JSON.
12. Run `scripts/generate_estimate_xlsx.py` to create the Excel workbook.
13. Report the workbook path, total base days, Buff days, final days, quotation amount, and highest-risk assumptions.

## Required Questions

Ask for project mode, included terminals, UI scope, person-day price, role-specific prices if any, quotation coefficient, standard-product coverage, third-party integrations, data migration, deployment/app publishing, and acceptance/training/documentation/support scope.

If the user cannot answer, continue with a clear default assumption and add the item to the customer confirmation questions.

## Estimation Rules

- Do not merge iOS, Android, Web admin, H5, mini program, and PC Web into one frontend field.
- Mark inferred coverage as pending confirmation unless the source requirement or user explicitly confirms it.
- Prefer function-level Buff. Use project-level Buff only when the requirement is too coarse. Never apply both to the same scope.
- Use Chinese sheet names and Chinese column headers in generated workbooks.
- Distinguish customer-readable function quotation from internal implementation details.
- Separate internal base effort from customer quotation. Do not hide risk, Buff, or quotation coefficient inside unexplained totals.

## Output

Generate an `.xlsx` workbook by default. Also summarize:

- 基础总人天
- Buff 总人天
- 最终总人天
- 客户报价金额
- 最高风险假设
- 待客户确认的问题数量
