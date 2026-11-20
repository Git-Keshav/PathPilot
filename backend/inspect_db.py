import asyncio
import asyncpg
import sys

# Ensure UTF-8 output in Windows terminal
sys.stdout.reconfigure(encoding='utf-8')

async def main():
    conn = await asyncpg.connect("postgresql://postgres:9045@localhost:5432/postgres")
    tables = await conn.fetch("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public' AND table_type = 'BASE TABLE'
        ORDER BY table_name;
    """)
    
    print(f"=== POSTGRESQL DATABASE SUMMARY ({len(tables)} tables) ===\n")
    
    for t in tables:
        tname = t["table_name"]
        count = await conn.fetchval(f'SELECT count(*) FROM "{tname}"')
        print(f"==================================================")
        print(f"TABLE: {tname} (Total Rows: {count})")
        print(f"==================================================")
        
        if count > 0:
            rows = await conn.fetch(f'SELECT * FROM "{tname}" LIMIT 20')
            for idx, r in enumerate(rows, 1):
                row_dict = {}
                for k, v in dict(r).items():
                    val_str = str(v)
                    if len(val_str) > 70:
                        val_str = val_str[:67] + "..."
                    row_dict[k] = val_str
                print(f"  [{idx}] {row_dict}")
            if count > 20:
                print(f"  ... ({count - 20} more rows)")
        else:
            print("  (0 records)")
        print()

    await conn.close()

if __name__ == "__main__":
    asyncio.run(main())
