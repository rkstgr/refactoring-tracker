import { LinearClient } from "@linear/sdk";
import { readFileSync } from "fs";

const client = new LinearClient({
    apiKey: process.env.LINEAR_API_KEY,
});

const TEAM_ID = process.env.TEAM_ID!;

const mainIssueResponse = await client.createIssue({
    title: "Refactor sql procedures",
    description: "",
    teamId: TEAM_ID,
});

const mainIssue = await mainIssueResponse.issue;

if (!mainIssue) {
    throw new Error("Could not create main issue");
} else {
    console.log("Main issue created successfully");
}

// Read the grouped data from JSON file
const groupedData = JSON.parse(
    readFileSync("../grouped_procedures.json", "utf8")
);

console.log(`Inserting ${groupedData.length} issues. This may take a bit...`);

await groupedData.forEach(async (procedure) => {
    const description = procedure.occurences
        .map((occurence) => {
            return `- ${occurence[0]} (${occurence[1]})`;
        })
        .join("\n");

    const issue = await client.createIssue({
        title: `${procedure.procedure_name}`,
        description: description,
        parentId: mainIssue.id,
        teamId: TEAM_ID,
    });
});
