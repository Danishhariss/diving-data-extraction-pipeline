from scraper import run_scraper
from transform import build_dataframe, export_outputs
from config import OUTPUT_CSV, OUTPUT_EXCEL


def main():
    print("Starting diving data extraction pipeline...")

    records = run_scraper()

    if not records:
        print("No structured records extracted yet.")
        print("Debug files generated for HTML inspection.")
        return

    print(f"Total records extracted: {len(records)}")

    df = build_dataframe(records)

    print("\nStructured Data Preview:")
    print(df.head())

    export_outputs(df, OUTPUT_CSV, OUTPUT_EXCEL)

    print("\nPipeline completed successfully.")


if __name__ == "__main__":
    main()