class UseCaseGenerationAgent:
    """
    Use Case Agent dynamically generates use cases based on AI trend data provided externally.
    """
    def __init__(self, ai_trend_data):
        self.ai_trend_data = ai_trend_data

    def run(self, inputs):
        industry = inputs.get('industry')

        # Dynamically retrieve AI trends for the given industry
        trends = self.ai_trend_data.get(industry, [])

        # Generate use cases dynamically based on trends
        use_cases = []
        for trend in trends:
            if 'chatbot' in trend.lower():
                use_cases.append("AI-powered customer support chatbots")
            elif 'predictive' in trend.lower():
                use_cases.append("Predictive maintenance using machine learning")
            elif 'report' in trend.lower():
                use_cases.append("Automated report generation with GenAI")
            elif 'supply chain' in trend.lower():
                use_cases.append("Supply chain optimization through AI")
            elif 'personalized' in trend.lower():
                use_cases.append("Personalized marketing using AI-driven insights")

        if not use_cases:
            # Fallback use cases if no trends match
            use_cases = [
                "AI-powered customer support chatbots",
                "Predictive maintenance using machine learning",
                "Automated report generation with GenAI",
                "Supply chain optimization through AI",
                "Personalized marketing using AI-driven insights"
            ]

        rationale = f"Use cases based on AI trends: {', '.join(trends)}"

        return {
            'use_cases': use_cases,
            'rationale': rationale
        }