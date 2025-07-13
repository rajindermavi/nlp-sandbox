import os
import pandas as pd
import asyncio
import cognee
from cognee.shared.logging_utils import get_logger, ERROR
from cognee.api.v1.visualize.visualize import visualize_graph
from cognee.api.v1.search import SearchType
from cognee.modules.engine.models import NodeSet


async def main():
    await cognee.prune.prune_data()
    await cognee.prune.prune_system(metadata=True)

    source_db = "sources_db"
    filedir = os.listdir(source_db + "/api_sources/api_source_docs")
    print(filedir)
    filename = filedir[0]
    print(filename)
    # load data
    data = pd.read_csv(source_db + "/api_sources/api_source_docs/" + filename)
    print('shape',data.shape)
    # add to cognee
    for idx, row in data.iterrows():
        # if you'd like to add just one doc at a time, control it from here
        node_set = ["docs", row["node_set_category"]]
        await cognee.add(row["content"], node_set=node_set)            
    print('rows added')
    await cognee.cognify()
    print('cognified')
    visualization_path = os.path.join(
        os.path.dirname(__file__), "./.artifacts/graph_visualization.html"
    )
    await visualize_graph(visualization_path)


async def cognify_with_ontology(ontology_path):
    # Cognify with optional ontology
    return await cognee.cognify(ontology_file_path=ontology_path)


async def search_cognee():
    answer = await cognee.search(
        query_text="What API endpoints are in the Ticketmaster api? Give me specific endpoint urls.",
        query_type=SearchType.GRAPH_COMPLETION,
        node_type=NodeSet,
        node_name=['developer.ticketmaster.com']
    )
    return answer


if __name__ == "__main__":
    logger = get_logger(level=ERROR)
    loop = asyncio.new_event_loop()
    asyncio.run(main())
    # add ontology
    asyncio.run(cognify_with_ontology("api_spec_ontology.owl"))
    # search
    #results = asyncio.run(search_cognee())
    #print(results[0])