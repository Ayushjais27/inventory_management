<script>
    document.addEventListener("DOMContentLoaded", function () {
        // Fetch inventory data and populate table
        fetch("/get_inventory")
            .then(response => response.json())
            .then(data => {
                const tableBody = document.getElementById("inventoryTable").getElementsByTagName("tbody")[0];
                const categoryFilter = document.getElementById("categoryFilter");

                // Clear table and dropdown
                tableBody.innerHTML = "";
                const categories = new Set();

                // Populate table rows and collect categories
                for (const item of Object.values(data)) {
                    const row = document.createElement("tr");

                    row.innerHTML = `
                        <td>${item.name}</td>
                        <td>${item.category}</td>
                        <td>${item.stock}</td>
                        <td>$${item.price.toFixed(2)}</td>
                    `;

                    tableBody.appendChild(row);
                    categories.add(item.category);
                }

                // Populate category dropdown
                categoryFilter.innerHTML = '<option value="">All Categories</option>';
                categories.forEach(category => {
                    const option = document.createElement("option");
                    option.value = category;
                    option.textContent = category;
                    categoryFilter.appendChild(option);
                });
            })
            .catch(error => console.error("Error loading inventory:", error));
    });

    function filterTable() {
        const searchInput = document.getElementById("searchInput").value.toLowerCase();
        const categoryFilter = document.getElementById("categoryFilter").value;
        const table = document.getElementById("inventoryTable");
        const rows = table.getElementsByTagName("tr");

        for (let i = 1; i < rows.length; i++) {
            const cells = rows[i].getElementsByTagName("td");
            const itemName = cells[0].textContent.toLowerCase();
            const category = cells[1].textContent;

            // Check search and filter criteria
            const matchesSearch = itemName.includes(searchInput);
            const matchesCategory = categoryFilter === "" || category === categoryFilter;

            // Show or hide the row
            rows[i].style.display = matchesSearch && matchesCategory ? "" : "none";
        }
    }
</script>
