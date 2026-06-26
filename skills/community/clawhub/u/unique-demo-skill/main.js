const sampleData = [
  { id: 1, name: "Example A", status: "active" },
  { id: 2, name: "Example B", status: "inactive" },
  { id: 3, name: "Example C", status: "active" },
];

console.log("Processing Sample Data:");
const activeItems = sampleData.filter(item => item.status === "active");
activeItems.forEach(item => console.log(`ID: ${item.id}, Name: ${item.name}`));