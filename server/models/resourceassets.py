class ResourceAssetAgent:
    """
    Resource Asset Agent uses DatasetSearchTool to dynamically find resources based on use cases.
    """
    def __init__(self, dataset_search_tool):
        self.dataset_search_tool = dataset_search_tool

    def run(self, inputs):
        use_cases = inputs.get('use_cases', [])
        resources = {}

        # Dynamic dataset search for each use case
        for case in use_cases:
            results = self.dataset_search_tool.search(case + " dataset")
            resources[case] = results.get('links', [])

        markdown_list = ""
        for case, links in resources.items():
            markdown_list += f"### {case}\n"
            if links:
                for link in links:
                    markdown_list += f"- [{link['title']}]({link['url']})\n"
            else:
                markdown_list += "- No relevant datasets found.\n"
            markdown_list += "\n"

        return {
            'resource_markdown': markdown_list
        }