// Copyright (c) 2024, Amandeep and contributors
// For license information, please see license.txt

let color = {
	absent: "#ff0044",
	leaves: "#3352FF",
	joining_date: "#808080",
	half_day: "#8b0a50",
	present: "#00FF00",
};

frappe.ui.form.on("Frappe Employee Attendance Heatmap", {
	employee: function (frm) {
		get_attendance_data(frm);
	},
	refresh: function (frm) {
		if (!frm.is_new()) {
			get_attendance_data(frm);
		}
	},
});

function get_attendance_data(frm) {
	frappe.call({
		method: "get_dates_of_entire_year",
		args: {
			employee: frm.doc.employee,
		},
		doc: frm.doc,
		callback: function (response) {
			if (response && response.message) {
				generate_heatmap(response);
			}
		},
	});
}

function generate_heatmap(response) {
	let all_dates = response.message;
	new frappe.Chart("#heatmap", {
		type: "heatmap",
		title: "Attendance Heatmap",
		data: {
			dataPoints: all_dates,
			start: new Date(Object.keys(all_dates)[0]),
			end: new Date(Object.keys(all_dates)[Object.keys(all_dates).length - 1]),
		},
		colors: [
			color["absent"],
			color["leaves"],
			color["joining_date"],
			color["half_day"],
			color["present"],
		],
	});
	add_custom_legend();
}

function add_custom_legend() {
    // Hide the default legend
    let style = document.createElement('style');
    style.textContent = '.frappe-chart.chart .chart-legend { display: none !important; }';
    document.head.appendChild(style);

    // Creating legend items
    let legendItems = [
        { color: color["absent"], label: 'Absent' },
        { color: color["present"], label: 'Present' },
        { color: color["leaves"], label: 'Leaves' },
        { color: color["joining_date"], label: 'Before Joining and Future Days' },
		{ color: color["half_day"], label: 'Half Day'}
    ];

	create_legend(legendItems);
}

function create_legend(legendItems) {
	let legendContainer = document.createElement('div');
    legendContainer.className = 'custom-legend';
    legendContainer.style.fontSize = '12px';

    legendItems.forEach(item => {
        let legendItem = document.createElement('div');
        legendItem.className = 'legend-item';
        legendItem.innerHTML = `<span class="legend-color-box" style="background-color:${item.color};width:20px;height:20px;">&nbsp;&nbsp;&nbsp;&nbsp;</span>`;
        legendItem.innerHTML += `<span class="legend-label" style="margin-left: 10px;">${item.label}</span>`;
        legendContainer.appendChild(legendItem);
    });

    let heatmapContainer = document.getElementById('heatmap');
    if (heatmapContainer) heatmapContainer.appendChild(legendContainer);
}
