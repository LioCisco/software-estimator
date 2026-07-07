# 输出 Schema

生成 Excel 前，先整理为 JSON。Excel 使用中文 Sheet 名和中文表头。

## 顶层字段

```json
{
  "project": {},
  "pricing": {},
  "summary": {},
  "functions": [],
  "implementation_details": [],
  "risks": [],
  "confirmation_questions": []
}
```

## project

- `name`: 项目名称
- `business_domain`: 业务领域
- `scope`: 估算范围
- `included_terminals`: 涉及端数组
- `estimation_mode`: 从零开发 / 标品二开 / 旧系统改造
- `excluded_scope`: 不含范围
- `key_assumptions`: 关键假设数组

## pricing

- `pricing_mode`: unified / role_based
- `person_day_price`: 统一人天单价；生成报价金额前必须由用户明确提供
- `quotation_coefficient`: 报价系数；可建议 1.2，但必须经用户确认
- `role_prices`: 角色单价映射，可为空
- `currency`: 默认 CNY

## summary

- `base_total_days`: 基础总人天
- `buff_total_days`: Buff 总人天
- `final_total_days`: Buff 后总人天
- `average_buff_percent`: 平均 Buff 比例
- `buff_reason_summary`: Buff 原因汇总
- `internal_estimated_amount`: 内部估算金额
- `customer_quotation_amount`: 客户报价金额
- `project_level_buff_applied`: 是否使用项目级 Buff

## functions

每行对应客户可读的功能报价清单。

必填字段：

- `module`: 一级模块
- `function`: 二级功能
- `description`: 功能说明
- `included_terminals`: 涉及端数组
- `coverage_mode`: 标品覆盖 / 部分覆盖 / 全部定开 / 待确认
- `coverage_evidence`: 文档明确 / 行业知识库推断 / 用户确认 / 待确认
- `complexity`: L / M / H
- `risk_level`: 低 / 中 / 高
- `product_days`
- `ui_days`
- `ios_days`
- `android_days`
- `web_admin_days`
- `h5_days`
- `mini_program_days`
- `pc_web_days`
- `frontend_subtotal_days`
- `backend_days`
- `test_days`
- `project_management_days`
- `base_total_days`
- `buff_percent`
- `buff_days`
- `buff_reason`
- `final_total_days`
- `quotation_amount`
- `notes`

## implementation_details

- `module`
- `function`
- `item_type`: 页面 / 接口 / 数据模型 / 后台任务 / 权限 / 报表 / 第三方集成 / 配置
- `item_name`
- `terminal_type`: iOS / Android / 管理后台Web / H5 / 小程序 / PC Web / 服务端 / 开放API
- `role`: 产品 / UI / iOS / Android / Web前端 / H5前端 / 小程序前端 / 后端 / 测试 / 项目管理
- `base_days`
- `coverage_coefficient`
- `complexity_coefficient`
- `risk_coefficient`
- `final_base_days`
- `estimation_evidence`
- `pending_confirmation`

## risks

- `category`
- `description`
- `affected_module`
- `risk_level`
- `day_impact`
- `suggested_handling`
- `included_in_quotation`: 是 / 否

## confirmation_questions

- `category`
- `related_module`
- `question`
- `why_it_matters`
- `effort_impact_range`
- `default_assumption`
- `customer_answer`
- `affects_quotation`: 是 / 否

## Excel Sheets

1. `报价汇总`
2. `功能报价清单`
3. `实施明细`
4. `风险与假设`
5. `客户确认问题`
