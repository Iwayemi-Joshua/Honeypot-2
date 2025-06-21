// =============================
// CHART.JS MOCK DATA SETUP
// =============================
const barCtx = document.getElementById("barChart").getContext("2d");
const pieCtx = document.getElementById("pieChart").getContext("2d");

let barChart = new Chart(barCtx, {
  type: "bar",
  data: {
    labels: ["Port Scan", "SQL Injection", "Brute Force", "DDoS"],
    datasets: [{
      label: "Attack Frequency",
      backgroundColor: ["#1f6f43", "#009688", "#4caf50", "#8bc34a"],
      data: [0, 0, 0, 0]
    }]
  },
  options: {
    responsive: true,
    plugins: {
      legend: { display: false }
    },
    scales: {
      y: {
        beginAtZero: true,
        ticks: { color: "#e0e0e0" },
        grid: { color: "#333" }
      },
      x: {
        ticks: { color: "#e0e0e0" },
        grid: { color: "#333" }
      }
    }
  }
});

let pieChart = new Chart(pieCtx, {
  type: "pie",
  data: {
    labels: ["Port Scan", "SQL Injection", "Brute Force", "DDoS"],
    datasets: [{
      backgroundColor: ["#1f6f43", "#009688", "#4caf50", "#8bc34a"],
      data: [0, 0, 0, 0]
    }]
  },
  options: {
    responsive: true,
    plugins: {
      legend: {
        labels: { color: "#e0e0e0" }
      }
    }
  }
});

// =============================
// Update charts from /events
// =============================
async function updateCharts() {
  const res = await fetch("/events");
  const data = await res.json();

  const typeCounts = { "Port Scan": 0, "SQL Injection": 0, "Brute Force": 0, "DDoS": 0 };

  (data.events || []).forEach(e => {
    if (typeCounts[e.type] !== undefined) {
      typeCounts[e.type]++;
    }
  });

  const values = Object.values(typeCounts);
  barChart.data.datasets[0].data = values;
  pieChart.data.datasets[0].data = values;

  barChart.update();
  pieChart.update();
}

updateCharts();
setInterval(updateCharts, 10000);
