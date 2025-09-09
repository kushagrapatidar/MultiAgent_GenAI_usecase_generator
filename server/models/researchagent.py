class ResearcherAgent:
    """
    Research Agent dynamically uses web search tool to fetch real-time info
    """
    def __init__(self, search_tool):
        self.search_tool = search_tool

    def run(self, inputs):
        company = inputs.get('company')
        industry = inputs.get('industry')

        # Dynamic search queries based on inputs
        industry_queries = [
            f"{industry} industry report 2025",
            f"{industry} market trends",
            f"{industry} strategic focus areas"
        ]
        company_queries = [
            f"{company} company profile",
            f"{company} key offerings",
            f"{company} AI strategy"
        ]

        # Real web search results
        industry_results = self.search_tool.search(industry_queries)
        company_results = self.search_tool.search(company_queries)

        # Summarize by concatenating found titles (can extend with NLP summarization)
        summary = "Industry insights:\n" + ", ".join(link['title'] for link in industry_results['links']) + "\n"
        summary += f"Company {company} info:\n" + ", ".join(link['title'] for link in company_results['links'])

        references = industry_results['links'] + company_results['links']

        return {
            'summary': summary,
            'references': references
        }