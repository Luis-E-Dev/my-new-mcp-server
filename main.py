"""
Salesforce Basic MCP Server to fetch Salesforce data
"""
import os
from mcp.server.fastmcp import FastMCP
from simple_salesforce import Salesforce
from dotenv import load_dotenv

#Load environment variables from .env file
load_dotenv()

#Initialize MCP server
mcp = FastMCP("salesforce-basic")

def get_salesforce_connection():
    return Salesforce(username=os.getenv("SF_USERNAME"),
                      password=os.getenv("SF_PASSWORD"),
                      security_token=os.getenv("SF_SECURITY_TOKEN"),
                      domain=os.getenv("SF_DOMAIN", "login")
    )

#Tool 1: Get Accounts
@mcp.tool()
def get_account(account_id: str) -> dict:
    sf = get_salesforce_connection()
    try:
        account = sf.Account.get(account_id)
        return {
            "success": True,
            "account": account
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

#Tool 2: Search Accts by Name
@mcp.tool()
def search_accounts(name: str) -> dict:
    sf = get_salesforce_connection()
    try:
        query = f"SELECT Id, Name, BillingAddress, Type, Industry FROM Account WHERE Name LIKE '%{name}%' LIMIT 10"
        result = sf.query(query)
        return {
            "success": True,
            "accounts": result['records'],
            "count": result['totalSize']
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

#Tool 3: Get recent Opportunities
@mcp.tool()
def get_recent_opportunities(limit: int = 5) -> dict:
    sf = get_salesforce_connection()
    try:
        query = f"SELECT Id, Name, StageName, Amount, CloseDate FROM Opportunity ORDER BY CreatedDate DESC LIMIT {limit}"
        result = sf.query(query)
        return {
            "success": True,
            "count": result["totalSize"],
            "opportunities": result['records']
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

#Run server
if __name__ == "__main__":
    mcp.run()
    