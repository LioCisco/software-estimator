# Software Estimator Skill

`software-estimator` is a Codex Skill for software development effort estimation and customer quotation. It reads requirements from documents, spreadsheets, images, or chat descriptions, decomposes the scope into functions, estimates multi-terminal effort, and generates a Chinese Excel workbook with quotation, Buff time, risks, assumptions, and customer confirmation questions.

## Use Cases

- Break customer requirements into a structured function list.
- Estimate effort for iOS, Android, Web admin, H5, mini program, PC Web, backend, and open APIs.
- Classify each function as standard covered, partially covered, fully custom, or pending confirmation.
- Generate a customer-readable quotation list.
- Generate internal implementation details for review.
- Output risks, assumptions, Buff time, and customer confirmation questions.

## Directory Structure

```text
software-estimator/
  SKILL.md
  agents/
    openai.yaml
  references/
    output-schema.md
    estimation-baseline.md
    coverage-rules.md
    risk-rules.md
    buff-rules.md
    knowledge/
      common-modules.md
      ecommerce.md
      erp-inventory.md
      crm.md
      finance.md
      oa-approval.md
  scripts/
    validate_estimate_data.py
    generate_estimate_xlsx.py
  examples/
    ecommerce.md
    sample_estimate.json
```

## Workflow

1. Read the requirement source.
2. Identify the business domain.
3. Identify included terminals: iOS, Android, Web admin, H5, mini program, PC Web, open API, and backend.
4. Ask mandatory prerequisite questions: unified person-day price or role-specific prices, quotation coefficient, project mode, included terminals, standard-product base, and existing system scope.
5. Split first-level modules and second-level functions.
6. Split internal implementation details.
7. Classify standard-product coverage.
8. Estimate complexity and risk level.
9. Calculate base effort by role and terminal.
10. Calculate Buff time and Buff reason separately.
11. Generate the Excel quotation workbook.
12. Generate customer confirmation questions.

## Excel Output

The default workbook contains 5 sheets:

- `报价汇总`: project scope, total effort, Buff, internal estimate amount, and customer quotation amount.
- `功能报价清单`: customer-readable function list with multi-terminal effort, Buff, and quotation amount.
- `实施明细`: internal implementation breakdown by page, API, data model, permission, report, third-party integration, and configuration.
- `风险与假设`: risks such as unclear requirements, third-party APIs, data migration, payment reconciliation, and assumptions.
- `客户确认问题`: customer questions and their effort impact.

## Estimation Model

There is no default person-day price. The skill must not reuse the `1200 CNY/person-day` sample value unless the user explicitly provides it in the current task. The skill may suggest a quotation coefficient of `1.2`, but it must ask the user before applying it.

Base formula:

```text
Base person-days = role baseline person-days * coverage coefficient * complexity coefficient * risk coefficient
Buff person-days = base total person-days * Buff percentage
Final person-days = base total person-days + Buff person-days
Unified-price quotation = final person-days * person-day price * quotation coefficient
```

If role-specific prices are provided:

```text
Role-based quotation = sum(role final person-days * role person-day price) * quotation coefficient
```

## Buff Rules

Buff is reserved time outside the base effort and must include an explicit reason. Default ranges:

- `0%-5%`: clear requirements, high standard-product coverage, no complex third-party integration.
- `5%-10%`: some pending requirements, multi-terminal adaptation, or a few third-party integrations.
- `10%-20%`: incomplete scope boundaries, data migration, complex permissions, complex reports, payment/refund/reconciliation.
- `20%-30%`: many pending requirements, legacy-system modification, complex business flow, strong external dependencies.

Prefer function-level Buff. Use project-level Buff only when the requirements are too coarse. Do not apply function-level Buff and project-level Buff to the same scope.

## Industry Knowledge Base

The first version includes:

- Common modules: login, organization, permission, data permission, notifications, logs, import/export, reports, deployment.
- Ecommerce: product, order, member, marketing, payment, logistics, after-sales, distribution, page decoration, reports.
- ERP/inventory: purchase, sales, inventory, warehouse, supplier, customer, document workflow.
- CRM: leads, customers, opportunities, follow-up, contracts, collection, sales funnel.
- Finance: receivable/payable, voucher, ledger, reports, reconciliation, expense, assets.
- OA/approval: organization, permission, approval flow, announcement, workflow forms, attendance, reimbursement.

The knowledge base is an estimation baseline, not final truth. Any coverage not explicitly confirmed by the requirement source or user must be marked as inferred or pending confirmation.

## Scripts

Validate estimate JSON:

```bash
python3 software-estimator/scripts/validate_estimate_data.py software-estimator/examples/sample_estimate.json
```

Generate Excel:

```bash
python3 software-estimator/scripts/generate_estimate_xlsx.py \
  software-estimator/examples/sample_estimate.json \
  outputs/software-estimator-sample.xlsx
```

Validate the skill:

```bash
python3 /Users/ciscomario/.codex/skills/.system/skill-creator/scripts/quick_validate.py software-estimator
```

## Sample Output

Sample data:

```text
software-estimator/examples/sample_estimate.json
```

Sample workbook:

```text
outputs/software-estimator-sample.xlsx
```
