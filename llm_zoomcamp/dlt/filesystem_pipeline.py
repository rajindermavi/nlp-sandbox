import dlt
import os


@dlt.resource(table_name="api_source_docs", max_table_nesting=0)
def get_data(files):
    for file in files:
        if not file.endswith(".txt"):
            continue
        print("Getting", file, "\n")
        with open(file, "r", encoding="utf-8") as f:
            content = f.read()
        filename = file.split("/")[-1]
        print(filename)
        source = filename.split(".")[1]
        print(source)
        yield {
                "source_name": source, # like api.slack.com
                "node_set_category": source, # like api.slack.com
                "filename": filename, # filename
                "content": content  # content of the page
        }


if __name__ == "__main__":
    # MY CUSTOM FILES
    source_locations = [
        "data/api.slack.com.txt",
        "data/api.monday.com.txt",
        "data/dev.paypal.com.txt"
    ]

    pipeline = dlt.pipeline(
        pipeline_name="api_doc_sources_pipeline",
        dataset_name="api_sources",
        destination="filesystem"
    )

    info = pipeline.run(get_data(source_locations), loader_file_format="csv")
    print(info)