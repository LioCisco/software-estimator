# Software Estimator 软件工时评估 Skill

`software-estimator` 是一个用于软件开发工时评估和客户报价的 Codex Skill。它可以从需求文档、Excel、图片或聊天描述中读取需求，拆分功能清单，估算多端工时，并生成带报价、Buff、风险和客户确认问题的中文 Excel。

## 适用场景

- 根据客户需求文档快速拆分功能清单
- 评估 iOS、Android、管理后台 Web、H5、小程序、PC Web、后端等多端工时
- 判断功能是否为标品覆盖、部分覆盖、全部定开或待确认
- 生成客户可读的报价清单
- 生成内部可复核的实施明细
- 输出风险、假设、Buff 时间和待客户确认问题

## 目录结构

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

## 固定流程

1. 读取需求内容。
2. 识别业务领域。
3. 识别涉及端：iOS、Android、管理后台 Web、H5、小程序、PC Web、开放 API、服务端。
4. 确认前置问题：人天单价、角色单价、是否从零开发、是否基于标品、已有系统范围等。
5. 拆分一级模块和二级功能。
6. 拆分内部实施明细。
7. 判断标品覆盖方式。
8. 评估复杂度和风险等级。
9. 计算各角色、各端基础工时。
10. 单独计算 Buff 时间和 Buff 原因。
11. 生成 Excel 报价文件。
12. 生成客户确认问题。

## Excel 输出

默认生成 5 个 Sheet：

- `报价汇总`：项目范围、总人天、Buff、内部估算金额、客户报价金额。
- `功能报价清单`：客户可读的功能清单，每个功能包含多端工时、Buff 和报价。
- `实施明细`：内部使用，按页面、接口、数据模型、权限、报表、第三方集成等拆分。
- `风险与假设`：列出需求不清、第三方接口、数据迁移、支付对账等风险。
- `客户确认问题`：列出报价前需要客户确认的问题和工时影响。

## 估算口径

基础公式：

```text
基础人天 = 角色基准人天 * 标品覆盖系数 * 复杂度系数 * 风险系数
Buff人天 = 基础合计人天 * Buff比例
最终人天 = 基础合计人天 + Buff人天
统一单价报价 = 最终人天 * 人天单价 * 报价系数
```

如果用户提供角色单价，则按角色分别计价：

```text
角色单价报价 = sum(角色最终人天 * 角色人天单价) * 报价系数
```

## Buff 规则

Buff 是基础工时之外的预留时间，必须单独说明原因。默认范围：

- `0%-5%`：需求清晰、标品覆盖高、无复杂第三方集成。
- `5%-10%`：部分需求待确认、多端适配、少量第三方接口。
- `10%-20%`：需求边界不完整、数据迁移、权限复杂、报表复杂、支付/退款/对账。
- `20%-30%`：大量需求待确认、旧系统改造、复杂业务流、强依赖外部接口。

优先使用功能级 Buff；只有需求太粗时才使用项目级 Buff。不要对同一范围重复叠加功能级 Buff 和项目级 Buff。

## 行业知识库

第一版内置以下知识库：

- 通用模块：登录、组织、权限、数据权限、消息、日志、导入导出、报表、部署等。
- 电商：商品、订单、会员、营销、支付、物流、售后、分销、装修、报表。
- ERP/进销存：采购、销售、库存、仓库、供应商、客户、单据流。
- CRM：线索、客户、商机、跟进、合同、回款、销售漏斗。
- 财务：应收应付、凭证、账簿、报表、对账、费用、资产。
- OA审批：组织、权限、审批流、公告、流程表单、考勤、报销。

行业知识库只作为估算基准。凡是文档没有明确说明的覆盖范围，都必须标注为推断或待确认。

## 使用脚本

校验估算 JSON：

```bash
python3 software-estimator/scripts/validate_estimate_data.py software-estimator/examples/sample_estimate.json
```

生成 Excel：

```bash
python3 software-estimator/scripts/generate_estimate_xlsx.py \
  software-estimator/examples/sample_estimate.json \
  outputs/software-estimator-sample.xlsx
```

验证 Skill：

```bash
python3 /Users/ciscomario/.codex/skills/.system/skill-creator/scripts/quick_validate.py software-estimator
```

## 样例输出

当前样例数据位于：

```text
software-estimator/examples/sample_estimate.json
```

样例 Excel 输出位于：

```text
outputs/software-estimator-sample.xlsx
```

