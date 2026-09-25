# Invoice Audit Exercise

Meridian Health Assurance Group reimburses five hospitals under five separately
negotiated service contracts. Each hospital submits invoices for the patients
it has treated. Some of those invoices are wrong — a rate that does not match
the contract, an adjustment applied when it was not due or omitted when it was,
a quantity beyond a contractual limit, a service billed twice.

# Medical Billing Auditing System

An automated pipeline designed to audit hospital invoices against complex, multi-format medical insurance contracts (structured tables, narrative texts, and multi-document amendments) using LLM-powered extraction, fuzzy string matching, and financial discrepancy detection.

---

## Project Structure & Architecture

The repository is organized into a clean, modular structure (`Modular Code`) alongside executable notebooks:

```text
insurance_auditing/
│
├── data/                      # Contains hospital contracts, raw invoices, and ground truth labels
│   ├── contracts/             # Hospital-specific contract folders (1 to 5)
│   ├── invoices/              # Invoice and line-item CSV files
│   └── labels/                # Development set ground-truth labels
│
├── notebooks/                 # Step-by-step Jupyter notebooks for EDA and auditing execution
│   ├── 01_eda_hospital_1.ipynb
│   ├── 02_audit_hospital.ipynb
│   └── 03_audit_hospitals.ipynb
│
├── src/                       # Core modular python scripts
│   ├── contract_parser.py     # LLM-based contract rule extraction engine
│   ├── item_mapper.py         # Fuzzy matching service mapping engine
│   └── auditor.py             # Financial auditing and discrepancy calculation engine
│
├── .env                       # API keys and environment configurations
├── requirements.txt           # Pinned library dependencies for reproducible execution
└── submission.csv             # Final aggregated multi-hospital audit results

```

---

## Tools & Technologies Used

* **Python:** Core programming language for pipeline implementation.
* **Pandas:** Data manipulation, cleaning, aggregation, and formatting of invoices and audit results.
* **Google Gemini API (`google-generativeai`):** LLM engine utilized for parsing unstructured narrative contracts and amendments into standardized rule JSONs.
* **RapidFuzz (`rapidfuzz`):** High-performance string matching library used for fuzzy mapping of colloquial invoice descriptions to official contract service catalogs.
* **Jupyter Notebooks & Python Modules:** For interactive exploration and modular, production-ready code structure.
* **Dotenv (`python-dotenv`):** Secure environment variable management.

---

## Solution Overview & Methodology

1. **Contract Parsing (`contract_parser.py`):** Utilizes Gemini to ingest unstructured or structured contract texts (including amendments and rate schedules) and extract pricing rules into standardized JSON formats (`contract_rules.json`).
2. **Fuzzy Item Mapping (`item_mapper.py`):** Bridges colloquial invoice descriptions with official contract nomenclature using token-ratio matching.
3. **Financial Auditing (`auditor.py`):** Computes expected line totals, aggregates invoice-level pricing, and applies error categorization (`Overbilled`, `Underbilled`, `Low Confidence Mapping`, or `Clean`).
4. **Safe Aggregation:** Automatically appends and merges multi-hospital results into a unified `submission.csv` without data loss.

---

## Results & Performance Summary

* **Validation Set (Hospital 1):** Achieved a 1.00 Recall, successfully capturing 100% of actual billing errors, complemented by systematic False Positive analysis to drive rigorous code-level mitigations.
* **Multi-Hospital Blind Sets (Hospitals 2 & 3):** Successfully processed a total of **2,989 invoices**, generating diagnostic health metrics, per-category error breakdowns, and safe append results into the final submission file.

---

## Acknowledgments & AI Assistance

We would like to acknowledge that artificial intelligence (specifically Google Gemini) was utilized as an assistive tool throughout this project to support drafting documentation (such as evaluation reports and decision logs) and writing specific code syntax and structuring. All architectural decisions, logical designs, and final validation were thoroughly reviewed and implemented by the project author.

```

```