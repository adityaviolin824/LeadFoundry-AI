# LeadFoundry AI

**Designed for fast, cost-efficient B2B contact discovery with auditable enrichment.**

LeadFoundry AI automates lead research by searching LinkedIn, Facebook, company websites, and Google Maps to find business contact information that matches user-defined criteria. It runs multiple searches in parallel, structures results into a clean Excel deliverable, and optionally emails the output when the run completes.

## Live Demo

* **API Backend**: WILL BE UP AND RUNNING SOON
* **Frontend UI**: 
* **Architecture**: Decoupled deployment with a FastAPI backend handling orchestration and a Streamlit frontend for live demo

<p align="center">
  <img src="templates/architecture_diagram_updated.png" 
       alt="Architecture Diagram"
       style="width:800px; height:500px; max-width:100%;">
</p>

## How It Works

### Query Generation

Users provide search criteria such as industry, location, personas, and keywords. An intake agent converts these inputs into 3–5 optimized search queries designed to maximize coverage while avoiding duplicate result sets. Each run includes at least one contact-focused query to surface pages containing email or phone information.

### Multi-Agent Research

Each query is distributed across four specialized agents running in parallel:

* **LinkedIn Agent**: Retrieves company profiles and business pages
* **Facebook Agent**: Locates business pages and public contact information
* **Website Agent**: Inspects company websites and extracts data from `/contact`, `/about`, and footer sections
* **Maps Agent**: Uses SERP API to extract business listings from Google Maps

Agents execute independently. Failures in one source do not block others, allowing the system to return partial but valid results when external services are unavailable.

### Structuring and Validation

Raw outputs from all agents are passed through a structuring layer that enforces a strict JSON schema. Each lead is normalized into consistent fields (`company`, `website`, `email`, `phone_number`, `location`, `description`). Missing values are explicitly set to `"unknown"`, and malformed responses are rejected.

### Deduplication and Sorting

Deduplication is handled deterministically in Python using company name and website as primary keys. Leads are ranked by contact completeness, prioritizing entries that contain both email and phone information.

### Enrichment

After initial consolidation, an enrichment step revisits leads with missing contact data. This stage fetches publicly accessible website pages such as contact pages, about pages, and footers to recover email addresses or phone numbers missed during the primary search. Enrichment is performed post-research to avoid slowing down the core pipeline.

Enrichment is best-effort and non-exhaustive. Some websites may block automated access, hide contact details behind client-side rendering, or deliberately obscure public contact information.

## Usage Modes

### With Email (Fire-and-Forget)

Designed for asynchronous use. Users submit a request, provide an email address, and close the browser. The pipeline runs in the background and sends the Excel output upon completion, even for long-running executions.

### Without Email (Interactive)

Users can monitor progress in real time through the UI, observe agent execution, preview intermediate results, and download the final output manually. This mode is primarily intended for testing and exploration.

## Performance Considerations

Execution time and API cost depend on agent count, query breadth, and enrichment depth. The system minimizes LLM usage by relying on deterministic Python logic wherever possible:

* Deduplication is algorithmic
* Sorting and ranking are rule-based
* Enrichment is triggered only for missing fields

This approach keeps runs cost-efficient while preserving output quality.

## Design Considerations and Model Selection Rationale

### Model Selection Strategy

Model choices were made based on iterative experimentation focused on lead quality, cost efficiency, and system-level output rather than single-run performance.

* **Research Agents**  
  Initial experiments showed that GPT-4.1-mini often produced higher-quality results in isolated runs. However, GPT-5-nano was selected for research agents due to significantly better lead value per dollar. While individual runs may be slightly weaker, the lower cost allows the system to issue more queries per run, resulting in broader coverage and a more comprehensive final lead list. In aggregate, this approach consistently outperformed fewer high-cost runs with stronger models.

* **Structuring Agent**  
  Lead structuring involves cross-domain reasoning, schema enforcement, and normalization across heterogeneous sources. GPT-4.1-mini was selected for this stage due to its higher consistency and reliability compared to GPT-4o-mini. This decision was informed by debugging and inspection using OpenAI trace analysis, where GPT-4.1-mini showed fewer malformed outputs and more stable schema adherence.

* **Query Generation**  
  Query generation is relatively low-cost and low-risk. GPT-4.1 was chosen as it demonstrated consistency comparable to GPT-4o while being significantly cheaper, and more stable than GPT-4o-mini in edge cases.

* **Enrichment**  
  Enrichment requires longer reasoning chains and multiple follow-up steps. GPT-4o was found to be prohibitively expensive for this purpose, while GPT-4o-mini showed higher variance and occasional hallucinated fields under extended runs. After increasing `max_turns` to 100 and testing multiple configurations, GPT-4.1-mini provided the best balance of cost, stability, and recovery of missing contact fields.

---

### Agent Effectiveness Observations

Based on empirical results across multiple runs, agent effectiveness was observed in the following order:

1. **Website Agent** (highest yield and contact accuracy)  
2. **Facebook Agent**  
3. **Google Maps Agent**  
4. **LinkedIn Agent**

This ordering reflects practical availability of public contact information rather than assumed platform importance.

---

### Extensibility and Enrichment Options

The system is designed to be modular. Agents can be added or removed based on target domain, geography, or data availability without impacting the core pipeline. For higher-quality enrichment, paid third-party APIs can be integrated selectively to improve coverage or precision where free sources are insufficient.

A conservative custom BeautifulSoup-based website scraper is also implemented as a fallback. It follows a strict skip-on-block policy to avoid timeouts, reduce failure cascades, and minimize legal or policy risks associated with aggressive scraping.

---

### Quantity vs Quality Tradeoffs

Lead discovery inherently involves a tradeoff between quantity and quality. The final default configuration reflects a balance informed by practical constraints and discussions with field marketing and sales managers. In many real-world outreach workflows, broader but cleanly structured lead lists are preferred over smaller, highly curated sets, provided contact validity and schema consistency are maintained.

As a result, the system prioritizes scalable coverage with deterministic post-processing, while allowing higher-cost, higher-precision enrichment paths to be enabled when required.


## Output Format

All leads conform to a fixed schema:

* company
* website
* email
* phone_number
* location
* description
* source
* source_urls

Results are delivered as `final_leads_list.xlsx`, containing deduplicated, enriched, and ranked leads ready for outreach.

## Technology Stack

* Python 3.12+
* FastAPI
* asyncio for parallel execution
* MCP (Model Context Protocol)
* DuckDuckGo Search MCP
* Tavily API
* SERP API
* Configurable LLM providers
* Docker
* Google Cloud Run
* Streamlit

## Deployment

The backend API is deployed on Google Cloud Run with request-driven autoscaling. The frontend UI is deployed separately on Streamlit Cloud. Both services are fully containerized and stateless, with each pipeline run assigned its own isolated directory for progress tracking and outputs.

## Legal and Data Use

The system uses official APIs and respects provider rate limits and usage policies. Only publicly available business contact information is processed.
