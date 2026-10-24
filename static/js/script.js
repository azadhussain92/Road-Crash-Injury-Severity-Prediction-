document.addEventListener('DOMContentLoaded', function() {
    // 1. Element References
    const latitudeInput = document.getElementById('latitude');
    const longitudeInput = document.getElementById('longitude');
    const timeOfCrashInput = document.getElementById('time_of_crash');
    const fetchSunDataBtn = document.getElementById('fetchSunDataBtn');
    const getLocationBtn = document.getElementById('getLocationBtn');

    // 2. SUN DATA LOGIC
    if (fetchSunDataBtn) {
        fetchSunDataBtn.addEventListener('click', fetchSunData);
        fetchSunDataBtn.disabled = !latitudeInput.value || !longitudeInput.value || !timeOfCrashInput.value;
    }
    const checkInputs = () => {
        if (fetchSunDataBtn) {
            if (latitudeInput.value && longitudeInput.value && timeOfCrashInput.value) {
                fetchSunDataBtn.disabled = false;
            } else {
                fetchSunDataBtn.disabled = true;
            }
        }
    };

    if (timeOfCrashInput) timeOfCrashInput.addEventListener('change', checkInputs);
    if (latitudeInput) latitudeInput.addEventListener('change', checkInputs);
    if (longitudeInput) longitudeInput.addEventListener('change', checkInputs);

    function fetchSunData() {
        const payload = {
            latitude: latitudeInput.value,
            longitude: longitudeInput.value,
            time_of_crash: timeOfCrashInput.value
        };
        fetch('/get_sun_data', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        })
        .then(response => response.json())
        .then(data => {
            if(data.sunrise) document.getElementById('sunriseTime').textContent = data.sunrise;
            if(data.sunset) document.getElementById('sunsetTime').textContent = data.sunset;
            if(data.light_condition) {
                document.getElementById('light_condition').value = data.light_condition;
            }
            const sunDataInfo = document.getElementById('sunDataInfo');
            if (sunDataInfo) sunDataInfo.classList.remove('hidden');
        })
        .catch(err => console.error("Error fetching sun data:", err));
    }

});