# FOFA 自然语言资产搜索 → 查询语句（华顺信安 参赛包 pkg-08e82c8d）

本仓库是「将自然语言资产搜索需求转换为 FOFA 查询语句」比赛的提交产物。

- 参赛包编号：`pkg-08e82c8d`
- 选手名称：林星宇
- 题目数量：100（`M001-S009` … `M100-S001`）
- 提交文件：[答案.json](答案.json)（UTF-8 JSON，题号与题目集完全一致，无缺题/重复/未知题号）

## 目录

```
答案.json              # 最终提交答案（100 条）
scripts/queries.py     # 题号 → 最终 FOFA Query 映射（唯一事实来源）
scripts/generate.py    # 由 queries.py 生成并校验 答案.json
```

## 作答规则（依据 README 参赛包要求）

- 每题只填一条**合法、完整、可执行**的 FOFA Query，不加解释或 Markdown。
- 无法转换时精确填写固定答案：`该需求不能直接转换为FOFA搜索语句`。
- 题号必须与题目集一一对应（100 题，不能缺题、重复或增加未知题号）。

## 方法

按 FOFA v5 官方字段与运算符能力表逐题映射，核心约定：

1. **运算符**：`=` 模糊包含（`=""` 表示字段不存在或为空）、`==` 完全匹配、`!=` 不等于、`*=` 通配（`?` 单字符）、`&&` / `||` / `()`；布尔字段只接受 `=true` / `=false` 且不加引号。
2. **字段映射**：IP/网段 → `ip`；端口 → `port`；根域/主机名 → `domain` / `host`；标题/正文/响应头 → `title` / `body` / `header`；服务响应原文 → `banner`；协议/传输层 → `protocol` / `base_protocol`；应用/产品/版本/门类 → `app` / `product` / `product.version` / `category`；地理 → `country` / `region` / `city`；证书 → `cert` / `cert.subject` / `cert.subject.org` / `cert.issuer.org` / `cert.issuer.cn` / `cert.domain` / `cert.sn` / `cert.is_valid` / `cert.is_match` / `cert.is_equal` / `cert.is_expired` / `cert.not_after.after|before`；TLS → `tls.version` / `tls.ja3s` / `jarm`；网站特征 → `icon_hash` / `fid` / `header_hash` / `body_hash` / `js_name` / `cname_domain`；标签 → `is_domain` / `is_ipv6` / `is_cloud` / `is_honeypot` / `is_fraud`。
3. **与/或优先级**：凡 `&&` 与 `||` 混用一律加括号，保证执行结果等于题面语义。
4. **否定条件**：仅在字段支持 `!=` 时使用（`is_*` / `cert.is_*` 等 `E` 类字段用 `=false` 表达否定）。
5. **应答兜底**：端口/网段值非法（如 `1000000`、`1.2.3.4.5`）、同字段自相矛盾、主观或需主机运行态数据的需求、纯能力咨询类问题，均填固定兜底句。

## 结果概览

- 94 题给出可执行 Query，6 题按规则填写兜底答案（M015、M091、M092、M093、M094、M095）。
- M097 的图标哈希按 FOFA 官方算法计算：favicon 字节 → Base64（`base64.encodebytes`，76 列换行）→ MurmurHash3 x86_32（seed 0，32 位有符号），得到 `-1493334710`。
- M096 的字段名取自 Jenkins 官方文档 *Exposed Services and Ports* → *TCP Agent Listener Port* 示例诊断响应：`Jenkins-Agent-Protocols`、`Jenkins-Version`、`Jenkins-Session`、`Remoting-Minimum-Version`。

## 重新生成与校验

```bash
python3 scripts/generate.py          # 重新生成 答案.json
python3 scripts/generate.py --check  # 校验题号完整性、非空与编码
```
